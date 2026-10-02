#!/usr/bin/env python3
"""Scrape all DaVita kidney-friendly recipes into a SQLite database.

Sources: https://davita.com/diet-nutrition/recipe-search/ (English)
         https://espanol.davita.com/dieta-nutricion/ (Spanish)
Data comes from the site's public WordPress REST API (recipes, nutrients,
taxonomies); the star rating is read from each recipe page's header.

Usage: python3 scrape_davita.py [--no-ratings] [--no-images]
Raw responses are cached in ./cache so reruns don't refetch.
"""
import html
import json
import re
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

import requests

# key, REST base, language, id offset (keeps ids unique across sites), cache prefix
SITES = [
    ("davita.com", "https://davita.com/wp-json/wp/v2", "en", 0, ""),
    ("espanol.davita.com", "https://espanol.davita.com/wp-json/wp/v2", "es", 1_000_000, "es_"),
]
HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
DB_PATH = HERE / "davita_recipes.db"
IMAGES = HERE / "images"
# Spanish category name -> English category, so both languages filter together
CATEGORY_EN = {
    "Bebidas": "Beverages", "Bocadillos y Snacks": "Appetizers & Snacks",
    "Carne de Res, Cordero y Cerdo": "Beef, Lamb & Pork", "Desayuno": "Breakfast & Brunch",
    "Ensaladas y Aderezos": "Salads & Dressings", "Marisco": "Fish & Seafood",
    "Panes": "Breads", "Pasta y Arroz": "Pasta, Rice & Grains",
    "Pizza y Sándwiches": "Pizza & Sandwiches", "Pollo y Pavo": "Chicken & Turkey",
    "Postres": "Desserts", "Salsas y Aderezos": "Sauces & Seasonings",
    "Sopas y Estofado": "Soups & Stews", "Verduras": "Vegetables",
}
UA = {"User-Agent": "Mozilla/5.0 (recipe-db research script)"}

TAXONOMIES = {
    "dv-recipe-category": "category",
    "dv-recipe-diet-tag": "diet_type",
    "dv-recipe-dish-type": "dish_type",
    "dv-recipe-cuisine-tag": "cuisine",
    "dv-recipe-holiday-tag": "holiday",
    "dv-recipe-method-tag": "cooking_method",
}

# meta key -> (column, unit)
NUTRIENTS = {
    "davita_calories": ("calories", ""),
    "davita_protein": ("protein_g", "g"),
    "davita_carbohydrates": ("carbohydrates_g", "g"),
    "davita_fat": ("fat_g", "g"),
    "davita_cholesterol": ("cholesterol_mg", "mg"),
    "davita_sodium": ("sodium_mg", "mg"),
    "davita_potassium": ("potassium_mg", "mg"),
    "davita_phosphorus": ("phosphorus_mg", "mg"),
    "davita_calcium": ("calcium_mg", "mg"),
    "davita_fiber": ("fiber_g", "g"),
    "davita_added_sugar": ("added_sugar_g", "g"),
}

session = requests.Session()
session.headers.update(UA)


def get(url, params=None, tries=5):
    for attempt in range(tries):
        try:
            r = session.get(url, params=params, timeout=60)
            if r.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"{r.status_code}")
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if attempt == tries - 1:
                raise
            wait = 2 ** attempt
            print(f"  retry {url} ({e}) in {wait}s", file=sys.stderr)
            time.sleep(wait)


def cached_json(name, url, params=None):
    path = CACHE / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    data = get(url, params).json()
    path.write_text(json.dumps(data), encoding="utf-8")
    return data


# ---------------------------------------------------------------- fetching

def fetch_terms(base, prefix):
    terms = []
    for tax in TAXONOMIES:
        page = 1
        while True:
            data = cached_json(f"{prefix}terms_{tax}_{page}", f"{base}/{tax}",
                               {"per_page": 100, "page": page})
            terms += [{**t, "taxonomy": tax} for t in data]
            if len(data) < 100:
                break
            page += 1
    return terms


def fetch_recipes(base, prefix):
    recipes, page = [], 1
    while True:
        params = {"per_page": 100, "page": page, "orderby": "id", "order": "asc"}
        path = CACHE / f"{prefix}recipes_{page}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
        else:
            r = session.get(f"{base}/dv-recipe", params=params, timeout=60)
            if r.status_code == 400:  # past the last page
                break
            r.raise_for_status()
            data = r.json()
            path.write_text(json.dumps(data), encoding="utf-8")
        recipes += data
        print(f"  recipes page {page}: {len(data)}")
        if len(data) < 100:
            break
        page += 1
    return recipes


RATING_RE = re.compile(
    r'aria-label="([\d.]+) [^"]*"\s*class="wp-block-dv-recipe-header__rating-star')


def fetch_rating(recipe):
    path = CACHE / "ratings" / f"{recipe['uid']}.txt"
    if path.exists():
        txt = path.read_text()
        return recipe["uid"], (float(txt) if txt else None)
    try:
        page = get(recipe["link"]).text
    except requests.RequestException as e:
        print(f"  rating fetch failed for {recipe['link']}: {e}", file=sys.stderr)
        return recipe["uid"], None
    m = RATING_RE.search(page)
    rating = float(m.group(1)) if m else None
    path.write_text("" if rating is None else str(rating))
    return recipe["uid"], rating


def fetch_ratings(recipes):
    (CACHE / "ratings").mkdir(exist_ok=True)
    ratings = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for i, (rid, rating) in enumerate(pool.map(fetch_rating, recipes), 1):
            ratings[rid] = rating
            if i % 100 == 0:
                print(f"  ratings: {i}/{len(recipes)}")
    return ratings


# ----------------------------------------------------------------- parsing

def clean(text):
    text = html.unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


class ContentParser(HTMLParser):
    """Split recipe body HTML into sections keyed by <h2> heading.

    Each section is a list of (group_label, text). <h3>/<h4> headings and
    paragraphs consisting only of bold text become group labels.
    """

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.sections = {}
        self.section = "_intro"
        self.group = None
        self.capture = None  # tag being captured: h2/h3/h4/li/p
        self.buf = []
        self.bold_only = True
        self.depth = 0  # nested list depth inside an li
        self.video = {}
        self._in_bold = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("strong", "b"):
            self._in_bold += 1
        if tag == "video" and a.get("data-poster"):
            self.video.setdefault("poster", a["data-poster"])
        elif tag == "source" and a.get("src"):
            self.video.setdefault("url", a["src"])
        elif tag == "track" and a.get("src"):
            self.video.setdefault("vtt", a["src"])
        elif tag == "iframe" and a.get("src"):
            self.video.setdefault("url", a["src"])

        if self.capture == "li" and tag in ("ul", "ol"):
            self.depth += 1
        elif self.capture is None and tag in ("h2", "h3", "h4", "li", "p"):
            self.capture, self.buf, self.bold_only = tag, [], True
        elif self.capture and tag == "br":
            self.buf.append(" ")

    def handle_endtag(self, tag):
        if tag in ("strong", "b"):
            self._in_bold = max(0, self._in_bold - 1)
        if self.capture == "li" and tag in ("ul", "ol") and self.depth:
            self.depth -= 1
            return
        if tag != self.capture:
            return
        text = clean("".join(self.buf))
        cap, self.capture = self.capture, None
        if not text:
            return
        if cap == "h2":
            self.section, self.group = text, None
        elif cap in ("h3", "h4") or (text.endswith(":") and (
                (cap == "p" and self.bold_only) or (cap == "li" and len(text) <= 40))):
            self.group = text.rstrip(":").strip()
        else:
            self.sections.setdefault(self.section, []).append((self.group, text))

    def handle_data(self, data):
        if self.capture:
            if data.strip() and not self._in_bold:
                self.bold_only = False
            self.buf.append(data)

    def handle_entityref(self, name):
        self.handle_data(f"&{name};")

    def handle_charref(self, name):
        self.handle_data(f"&#{name};")



def banner_url(base, prefix, media_id):
    """Fallback image: the recipe banner attachment when there is no featured image."""
    if not media_id:
        return None
    try:
        data = cached_json(f"{prefix}media_{media_id}", f"{base}/media/{media_id}")
    except requests.RequestException:
        return None
    return data.get("source_url")


def download_image(args):
    rid, url = args
    if not url:
        return rid, None
    ext = Path(url.split("?")[0]).suffix or ".jpg"
    path = IMAGES / f"{rid}{ext}"
    if not path.exists():
        try:
            path.write_bytes(get(url).content)
        except requests.RequestException as e:
            print(f"  image failed {url}: {e}", file=sys.stderr)
            return rid, None
    return rid, str(path.relative_to(HERE))


def find_section(sections, *names):
    for key, items in sections.items():
        k = key.lower()
        if any(n in k for n in names):
            return items
    return []


def to_float(v):
    try:
        return float(str(v).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def strip_size(url):
    return url.split("?")[0] if url else None


# ------------------------------------------------------------------ schema

SCHEMA = f"""
DROP TABLE IF EXISTS recipe_terms;
DROP TABLE IF EXISTS terms;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS steps;
DROP TABLE IF EXISTS hints;
DROP TABLE IF EXISTS food_choices;
DROP TABLE IF EXISTS recipe_sections;
DROP TABLE IF EXISTS recipes;
DROP VIEW IF EXISTS recipe_overview;

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,      -- wp_id, +1000000 for espanol.davita.com
    site TEXT NOT NULL,
    language TEXT NOT NULL,      -- en / es
    wp_id INTEGER NOT NULL,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    category TEXT,               -- as shown on the source site
    category_en TEXT,            -- English category (same for both languages)
    description TEXT,
    image_url TEXT,
    image_path TEXT,             -- local copy under ./images
    portions TEXT,
    serving_size TEXT,
    rating REAL,
    comment_count INTEGER,
    submitted_by TEXT,
    prep_time TEXT,
    cook_time TEXT,
    total_time TEXT,
    carbohydrate_choices TEXT,
    nutrition_footnote TEXT,
    {", ".join(f"{col} REAL, {col}_raw TEXT" for col, _ in NUTRIENTS.values())},
    video_url TEXT,
    video_poster TEXT,
    video_subtitles_url TEXT,
    date_published TEXT,
    date_modified TEXT,
    content_html TEXT,
    meta_json TEXT
);

CREATE TABLE terms (
    id INTEGER PRIMARY KEY,      -- wp term id, +1000000 for espanol.davita.com
    site TEXT NOT NULL,
    taxonomy TEXT NOT NULL,      -- category, diet_type, dish_type, cuisine, holiday, cooking_method
    name TEXT NOT NULL,
    slug TEXT,
    count INTEGER
);

CREATE TABLE recipe_terms (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id),
    term_id INTEGER NOT NULL REFERENCES terms(id),
    taxonomy TEXT NOT NULL,
    PRIMARY KEY (recipe_id, term_id)
);

CREATE TABLE ingredients (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id),
    position INTEGER NOT NULL,
    group_label TEXT,
    text TEXT NOT NULL
);
CREATE TABLE steps (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id),
    position INTEGER NOT NULL,
    group_label TEXT,
    text TEXT NOT NULL
);
CREATE TABLE hints (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id),
    position INTEGER NOT NULL,
    group_label TEXT,
    text TEXT NOT NULL
);
CREATE TABLE food_choices (      -- "Kidney and kidney diabetic food choices"
    recipe_id INTEGER NOT NULL REFERENCES recipes(id),
    position INTEGER NOT NULL,
    text TEXT NOT NULL
);
-- every <h2> section of the body, incl. any not covered above
CREATE TABLE recipe_sections (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id),
    section TEXT NOT NULL,
    position INTEGER NOT NULL,
    group_label TEXT,
    text TEXT NOT NULL
);

CREATE INDEX idx_ing ON ingredients(recipe_id);
CREATE INDEX idx_steps ON steps(recipe_id);
CREATE INDEX idx_hints ON hints(recipe_id);
CREATE INDEX idx_fc ON food_choices(recipe_id);
CREATE INDEX idx_rt_term ON recipe_terms(term_id);
CREATE INDEX idx_rec_cat ON recipes(category_en);

CREATE VIEW recipe_overview AS
SELECT r.id, r.language, r.title, r.category_en AS category, r.portions, r.serving_size, r.rating, r.comment_count,
       (SELECT group_concat(t.name, ', ') FROM recipe_terms rt JOIN terms t ON t.id = rt.term_id
         WHERE rt.recipe_id = r.id AND rt.taxonomy = 'diet_type') AS diet_types,
       r.calories, r.protein_g, r.carbohydrates_g, r.fat_g, r.cholesterol_mg, r.sodium_mg,
       r.potassium_mg, r.phosphorus_mg, r.calcium_mg, r.fiber_g, r.added_sugar_g,
       r.carbohydrate_choices, r.image_url, r.video_url, r.url
FROM recipes r;
"""


# -------------------------------------------------------------------- main

def main():
    CACHE.mkdir(exist_ok=True)
    terms, recipes = [], []
    for site, base, lang, off, prefix in SITES:
        print(f"[{site}] fetching taxonomies...")
        for t in fetch_terms(base, prefix):
            terms.append({**t, "uid": t["id"] + off, "site": site})
        print(f"[{site}] fetching recipes...")
        site_recipes = fetch_recipes(base, prefix)
        print(f"  {len(site_recipes)} recipes")
        for r in site_recipes:
            r.update(uid=r["id"] + off, site=site, lang=lang, off=off, base=base, prefix=prefix)
        recipes += site_recipes

    ratings = {}
    if "--no-ratings" not in sys.argv:
        print("Fetching ratings from recipe pages...")
        ratings = fetch_ratings(recipes)

    image_urls = {r["uid"]: strip_size((r.get("featured_image_src_large") or [None])[0])
                  or banner_url(r["base"], r["prefix"], r["meta"].get("davita_recipe_banner"))
                  for r in recipes}
    image_paths = {}
    if "--no-images" not in sys.argv:
        print("Downloading images...")
        IMAGES.mkdir(exist_ok=True)
        with ThreadPoolExecutor(max_workers=8) as pool:
            image_paths = dict(pool.map(download_image, image_urls.items()))

    term_by_id = {t["uid"]: t for t in terms}
    cat_tax = "dv-recipe-category"

    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA)
    db.executemany(
        "INSERT INTO terms VALUES (?,?,?,?,?,?)",
        [(t["uid"], t["site"], TAXONOMIES[t["taxonomy"]], clean(t["name"]), t["slug"], t["count"])
         for t in terms])

    nutrient_cols = [c for c, _ in NUTRIENTS.values()]
    cols = (["id", "site", "language", "wp_id", "slug", "title", "url", "category",
             "category_en", "description", "image_url", "image_path",
             "portions", "serving_size", "rating", "comment_count", "submitted_by",
             "prep_time", "cook_time", "total_time", "carbohydrate_choices",
             "nutrition_footnote"]
            + [x for c in nutrient_cols for x in (c, f"{c}_raw")]
            + ["video_url", "video_poster", "video_subtitles_url", "date_published",
               "date_modified", "content_html", "meta_json"])
    insert_recipe = f"INSERT INTO recipes ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})"

    for r in recipes:
        uid, off = r["uid"], r["off"]
        meta = r.get("meta") or {}
        content = r["content"]["rendered"]
        p = ContentParser()
        p.feed(content)
        p.close()
        sections = p.sections

        cats = [clean(term_by_id[t + off]["name"]) for t in r.get(cat_tax, []) if t + off in term_by_id]
        cats_en = [CATEGORY_EN.get(c, c) for c in cats]
        nutr = []
        for key, (col, _) in NUTRIENTS.items():
            raw = (meta.get(key) or "").strip()
            nutr += [to_float(raw), raw or None]

        row = ([uid, r["site"], r["lang"], r["id"], r["slug"], clean(r["title"]["rendered"]),
                r["link"], ", ".join(cats) or None, ", ".join(cats_en) or None,
                clean(re.sub(r"<[^>]+>", " ", r["excerpt"]["rendered"])) or None,
                image_urls[uid],
                image_paths.get(uid),
                clean(meta.get("davita_servings") or "") or None,
                clean(meta.get("davita_servings_size") or "") or None,
                ratings.get(uid) or None,  # 0 stars = not yet rated
                r.get("comment_info"),
                clean(meta.get("davita_submitted_by") or "") or None,
                meta.get("davita_prep_time") or meta.get("davita_gsc_prep_time") or None,
                meta.get("davita_cooking_time") or meta.get("davita_gsc_cook_time") or None,
                meta.get("davita_gsc_total_time") or None,
                clean(meta.get("davita_carbohydrate_choices") or "") or None,
                clean(re.sub(r"<[^>]+>", " ", meta.get("davita_nutrition_footnote") or "")) or None]
               + nutr
               + [p.video.get("url"), p.video.get("poster"), p.video.get("vtt"),
                  r["date"], r["modified"], content, json.dumps(meta)])
        db.execute(insert_recipe, row)

        for table, names in (("ingredients", ("ingredient",)),
                             ("steps", ("preparation", "preparaci", "direction", "instruction",
                                        "method", "instrucci")),
                             ("hints", ("hint", "tip", "consejo"))):
            items = find_section(sections, *names)
            db.executemany(f"INSERT INTO {table} VALUES (?,?,?,?)",
                           [(uid, i, g, t) for i, (g, t) in enumerate(items, 1)])

        for name, items in sections.items():
            db.executemany("INSERT INTO recipe_sections VALUES (?,?,?,?,?)",
                           [(uid, name, i, g, t) for i, (g, t) in enumerate(items, 1)])

        choices = [clean(x) for x in (meta.get("davita_kidney_diabetic_food_choices") or "").splitlines()]
        db.executemany("INSERT INTO food_choices VALUES (?,?,?)",
                       [(uid, i, c) for i, c in enumerate([c for c in choices if c], 1)])

        for tax, label in TAXONOMIES.items():
            for tid in r.get(tax, []) or []:
                if tid + off in term_by_id:
                    db.execute("INSERT OR IGNORE INTO recipe_terms VALUES (?,?,?)",
                               (uid, tid + off, label))

    db.commit()
    db.close()
    print(f"Saved {len(recipes)} recipes to {DB_PATH}")


if __name__ == "__main__":
    main()
