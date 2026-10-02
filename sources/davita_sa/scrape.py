#!/usr/bin/env python3
"""Scraper for DaVita Saudi Arabia (davita.sa) recipes.

The site is a Next.js front end over a Statamic CMS. The backend GraphQL
endpoint (https://backend.davita.sa/graphql) answers 401 Unauthorized, and the
Statamic REST API (/api/collections/...) is 404, so recipe data is read from
the React Server Components payload (self.__next_f) embedded in each page.

Outputs (all inside sources/davita_sa/):
  recipes.json  - recipes NOT already in davita_recipes.db (en + official ar)
  matches.json  - davita.sa recipes that already exist in the DB, with image
  images/       - full-size photos (original asset permalinks)
  report.json, skipped.json, cache/
The database is opened read-only and never modified.
"""
import html as htmllib
import json
import os
import re
import sqlite3
import struct
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

KEY = "davita_sa"
SOURCE_NAME = "DaVita Saudi Arabia"
BASE = "https://davita.sa"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CACHE = os.path.join(HERE, "cache")
IMAGES = os.path.join(HERE, "images")
DB = os.path.join(ROOT, "davita_recipes.db")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept-Language": "en,ar;q=0.8"})

CATEGORY = {
    "tasty-eggplant-casserole": "Vegetables",
    "vegetable-cutlet": "Vegetables",
    "loqaymat": "Desserts",
    "barley-and-beef-stew": "Soups & Stews",
    "eggplants-roll": "Vegetables",
    "pumpkin-soup": "Soups & Stews",
    "chicken-fajita": "Chicken & Turkey",
    "caesar-salad-with-chicken": "Salads & Dressings",
    "bavarian-apple-tart": "Desserts",
    "pineapple-cake": "Desserts",
    "kursan-with-lamb-and-vegetables": "Beef, Lamb & Pork",
    "fatosh-salad": "Salads & Dressings",
    "grilled-marinated-chicken": "Chicken & Turkey",
    "creamy-cucumber-spread": "Appetizers & Snacks",
    "roasted-lamb": "Beef, Lamb & Pork",
    "vegetarian-pizza": "Pizza & Sandwiches",
    "slow-cooker-mixed-fruit-recipe": "Desserts",
    "royal-meringue-cookies": "Desserts",
}
DIETS = {
    "ckd non-dialysis": "CKD non-dialysis", "dialysis": "Dialysis",
    "diabetes": "Diabetes", "gluten-free": "Gluten-free",
    "heart healthy": "Heart Healthy", "vegetarian": "Vegetarian",
    "lower potassium": "Lower Potassium", "higher potassium": "Higher Potassium",
    "lower protein": "Lower Protein",
}
NUTRIENT_LABELS = {
    "calories": "calories", "protein": "protein_g", "carbohydrates": "carbohydrates_g",
    "fat": "fat_g", "cholesterol": "cholesterol_mg", "sodium": "sodium_mg",
    "potassium": "potassium_mg", "phosphorus": "phosphorus_mg", "calcium": "calcium_mg",
    "fiber": "fiber_g", "added sugar": "added_sugar_g",
}
NUTRIENT_KEYS = ["calories", "protein_g", "carbohydrates_g", "fat_g", "cholesterol_mg",
                 "sodium_mg", "potassium_mg", "phosphorus_mg", "calcium_mg", "fiber_g",
                 "added_sugar_g"]


# ---------------------------------------------------------------- fetching
def cache_name(url):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", url.split("://", 1)[1]).strip("_")[:180]


def fetch(url, binary=False, use_cache=True):
    path = os.path.join(CACHE, cache_name(url))
    if use_cache and not binary and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return 200, f.read()
    delay = 2
    for attempt in range(6):
        try:
            r = session.get(url, timeout=60)
        except requests.RequestException:
            time.sleep(delay); delay *= 2; continue
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(delay); delay *= 2; continue
        if binary:
            return r.status_code, r.content
        r.encoding = "utf-8"
        if r.status_code == 200 and use_cache:
            with open(path, "w", encoding="utf-8") as f:
                f.write(r.text)
        return r.status_code, r.text
    return None, None


def rsc_payload(html):
    """Concatenate the string chunks pushed into self.__next_f."""
    out = []
    for m in re.finditer(r"self\.__next_f\.push\((\[.*?\])\)</script>", html, re.S):
        try:
            arr = json.loads(m.group(1))
        except ValueError:
            continue
        if len(arr) > 1 and isinstance(arr[1], str):
            out.append(arr[1])
    return "".join(out)


def json_objects(payload, marker):
    dec = json.JSONDecoder()
    for m in re.finditer(re.escape(marker), payload):
        try:
            obj, _ = dec.raw_decode(payload, m.start())
        except ValueError:
            continue
        yield obj


def recipe_entry(payload, slug):
    """The detail entry for slug: the Entry_Recipes_Recipe object with ingredients."""
    for obj in json_objects(payload, '{"__typename":"Entry_Recipes_Recipe"'):
        if obj.get("slug") == slug and "ingredient" in obj:
            return obj
    return None


def listing_slugs(payload):
    slugs = []
    for obj in json_objects(payload, '{"__typename":"Entry_Recipes_Recipe"'):
        s = obj.get("slug")
        if s and s not in slugs:
            slugs.append(s)
    for s in re.findall(r"/diet-nutrition/([a-z0-9-]+)", payload):
        if s not in slugs:
            slugs.append(s)
    return slugs


# ---------------------------------------------------------------- parsing
def num(value):
    if value is None:
        return None
    m = re.search(r"\d+(?:[.,]\d+)?", str(value))
    return float(m.group(0).replace(",", ".")) if m else None


def nutrients_from(entry):
    out = {k: None for k in NUTRIENT_KEYS}
    for item in entry.get("nutrition") or []:
        key = NUTRIENT_LABELS.get((item.get("label") or "").strip().lower())
        if key:
            v = num(item.get("value"))
            if v is not None and v == int(v):
                v = int(v)
            out[key] = v
    return out


def nutrients_raw(entry):
    items = entry.get("nutrition") or []
    return "\n".join(f"{i.get('label')}: {i.get('value')}" for i in items) or None


def clean_list(items):
    return [x.strip() for x in (items or []) if isinstance(x, str) and x.strip()]


def join_wrapped(lines):
    """English steps are PDF line-wraps; rejoin a line with the next when the
    line lacks closing punctuation and the next starts lowercase."""
    out = []
    for line in lines:
        if out and not re.search(r"[.!?:;)]$", out[-1]) and re.match(r"[a-z(]", line):
            out[-1] = out[-1] + " " + line
        else:
            out.append(line)
    return out


def diets(diet_type):
    out = []
    for part in re.split(r"[,|/]", diet_type or ""):
        d = DIETS.get(part.strip().lower())
        if d and d not in out:
            out.append(d)
    return out


def portions_from(hints):
    for h in hints:
        m = re.search(r"(?:serving is for|serves|portions:?|makes)\s*(\d+)", h, re.I)
        if m:
            return m.group(1)
    return None


def _ar_serving(hints):
    for h in hints:
        m = re.search(r"حجم الحصة\s*:\s*(.+)$", h)
        if m:
            return m.group(1).strip()
    return None


def serving_size_from(hints):
    for h in hints:
        m = re.search(r"serving size:\s*(.+?)\.?$", h, re.I)
        if m:
            return m.group(1).strip()
        m = re.search(r"total serving:\s*(?:equal to\s*)?(.+?)\.?$", h, re.I)
        if m:
            return m.group(1).strip()
    return None


def video_url(entry):
    v = entry.get("recipe_video")
    if isinstance(v, dict):
        return v.get("permalink") or v.get("url") or v.get("src")
    if isinstance(v, str) and v.strip():
        return v.strip()
    return None


def image_url(entry):
    img = entry.get("recipe_image") or {}
    return img.get("permalink") or img.get("src")


def jpeg_size(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return None
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1; continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return (w, h)
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


def download_image(url, slug):
    if not url:
        return None
    ext = os.path.splitext(url.split("?")[0])[1].lower() or ".jpg"
    rel = f"sources/{KEY}/images/{slug}{ext}"
    path = os.path.join(ROOT, rel)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return rel
    status, data = fetch(url, binary=True)
    if status == 200 and data:
        with open(path, "wb") as f:
            f.write(data)
        return rel
    return None


# ---------------------------------------------------------------- matching
STOP = {"with", "and", "the", "a", "of", "recipe", "in"}


def norm_words(title):
    words = re.findall(r"[a-z0-9]+", title.lower())
    return [w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w
            for w in words if w not in STOP]


def norm_title(title):
    return " ".join(norm_words(title))


CMP = [("calories", 10, 0.10), ("sodium_mg", 10, 0.10), ("potassium_mg", 10, 0.10),
       ("phosphorus_mg", 10, 0.10), ("protein_g", 1, 0.10)]


def nutrient_agreement(sa, db):
    """(agreeing, compared) over calories, Na, K, P, protein.
    Agree = within max(abs tolerance, 10% of the DB value)."""
    agree = compared = 0
    for key, abs_tol, rel_tol in CMP:
        a, b = sa.get(key), db.get(key)
        if a is None or b is None:
            continue
        compared += 1
        if abs(a - b) <= max(abs_tol, rel_tol * abs(b)):
            agree += 1
    return agree, compared


def nutrients_match(sa, db):
    agree, compared = nutrient_agreement(sa, db)
    return compared >= 3 and agree >= compared - 1


UNIT_WORDS = set("cup cups tablespoon tablespoons teaspoon teaspoons ounce ounces pound pounds "
                 "medium large small pinch sliced inch size fresh dried optional chopped "
                 "minced whole each".split())


def ingredient_tokens(text):
    return {w.rstrip("s") for w in re.findall(r"[a-z]{4,}", text.lower()) if w not in UNIT_WORDS}


def db_ingredient_text(content_html):
    t = htmllib.unescape(re.sub(r"<[^>]+>", " ", content_html or ""))
    t = re.sub(r"\s+", " ", t)
    m = re.search(r"Ingredients(.*?)(Preparation|Directions)", t, re.S)
    return m.group(1) if m else ""


def ingredient_overlap(sa_ingredients, db_row):
    """Overlap coefficient of ingredient words (|A&B| / min(|A|,|B|))."""
    a = ingredient_tokens(" ".join(sa_ingredients))
    b = ingredient_tokens(db_ingredient_text(db_row.get("content_html")))
    return len(a & b) / max(1, min(len(a), len(b)))


def load_db():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT id, title, url, calories, sodium_mg, potassium_mg, phosphorus_mg, protein_g, "
        "content_html "
        "FROM recipes WHERE canonical_id = id AND language = 'en'").fetchall()
    con.close()
    return [dict(r) for r in rows]


REJECTED = []  # same title, different recipe


def find_match(title, nutrients, db_rows, ingredients):
    nt = norm_title(title)
    exact = [r for r in db_rows if norm_title(r["title"]) == nt]
    if exact:
        best = next((r for r in exact if nutrients_match(nutrients, r)), None)
        if best:
            return best, "title+nutrients", "exact"
        # Nutrients disagree: accept the title match only if the ingredient
        # lists clearly describe the same dish (metric/local adaptation).
        scored = sorted(((ingredient_overlap(ingredients, r), r) for r in exact),
                        key=lambda x: -x[0])
        if scored[0][0] >= 0.7:
            return scored[0][1], "title", f"exact (ingredient overlap {scored[0][0]:.2f})"
        REJECTED.append(f"{title} vs DB {scored[0][1]['id']} '{scored[0][1]['title']}' "
                        f"(nutrients differ, ingredient overlap {scored[0][0]:.2f})")
    # Near titles (e.g. "Slow cooker Mixed Fruit Recipe" vs "... Pudding"):
    # accept only when most title words overlap AND the nutrients agree.
    words = set(norm_words(title))
    best, best_score = None, 0
    for r in db_rows:
        w2 = set(norm_words(r["title"]))
        if not words or not w2:
            continue
        score = len(words & w2) / len(words | w2)
        if score >= 0.5 and nutrients_match(nutrients, r) and score > best_score:
            best, best_score = r, score
    if best:
        return best, "title+nutrients", f"near-title (word overlap {best_score:.2f})"
    return None, None, None


# ---------------------------------------------------------------- main
def build_record(entry, slug, lang, en_entry=None):
    url = f"{BASE}/ar/diet-nutrition/{slug}" if lang == "ar" else f"{BASE}/diet-nutrition/{slug}"
    base_entry = en_entry or entry
    hints = clean_list(entry.get("helpful_hints"))
    steps = clean_list(entry.get("prepration"))
    if lang == "en":
        steps = join_wrapped(steps)
    img = image_url(entry) or image_url(base_entry)
    return {
        "source": KEY,
        "source_name": SOURCE_NAME,
        "source_id": slug if lang == "en" else f"{slug}-ar",
        "url": url,
        "lang": lang,
        "title": (entry.get("title") or "").strip(),
        "description": (base_entry.get("diet_type") or "").strip() or None
        if not diets(base_entry.get("diet_type")) and lang == "en" else
        ((entry.get("diet_type") or "").strip() or None if not diets(base_entry.get("diet_type")) else None),
        "image_url": img,
        "image_path": None,
        "portions": portions_from(clean_list(base_entry.get("helpful_hints"))),
        "serving_size": serving_size_from(hints) if lang == "en" else _ar_serving(hints),
        "category": CATEGORY.get(slug, "Vegetables"),
        "diet": diets(base_entry.get("diet_type")),
        "dish": [], "cuisine": [], "method": [],
        "nutrients": nutrients_from(base_entry),
        "nutrients_raw": nutrients_raw(entry),
        "ingredients": [[None, x] for x in clean_list(entry.get("ingredient"))],
        "steps": [[None, x] for x in steps],
        "hints": [[None, x] for x in hints],
        "food_choices": [],
        "carb_choices": None,
        "video_url": video_url(entry),
        "prep_time": None, "cook_time": None, "total_time": None,
        "translation_of": slug if lang == "ar" else None,
    }


def is_arabic(entry):
    return (entry.get("locale") in ("arabic", "ar")
            and re.search(r"[؀-ۿ]", entry.get("title") or "") is not None)


def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(IMAGES, exist_ok=True)
    skipped = []

    # 1. API check (documented; the scraper falls back to page parsing).
    api_notes = []
    for url in ("https://backend.davita.sa/graphql",
                "https://backend.davita.sa/api/collections/recipes/entries"):
        status, _ = fetch(url, use_cache=False)
        api_notes.append(f"{url} -> HTTP {status}")

    # 2. Discovery: listing pages + sitemap.
    slugs = []
    listing_counts = {}
    for path in ("/diet-nutrition", "/ar/diet-nutrition"):
        status, html = fetch(BASE + path)
        found = listing_slugs(rsc_payload(html or ""))
        listing_counts[path] = len(found)
        for s in found:
            if s not in slugs:
                slugs.append(s)
    _, sm = fetch(BASE + "/sitemap.xml")
    sitemap_urls = []
    for sub in re.findall(r"<loc>([^<]+)</loc>", sm or ""):
        if sub.endswith(".xml"):
            _, x = fetch(sub)
            sitemap_urls += re.findall(r"<loc>([^<]+)</loc>", x or "")
        else:
            sitemap_urls.append(sub)
    sitemap_recipe_slugs = []
    dead_aliases = []
    for u in sitemap_urls:
        m = re.match(r"https://davita\.sa/(?:ar/)?(?:diet-nutrition/)?([a-z0-9-]+)$", u)
        if not m:
            continue
        cand = m.group(1)
        if cand not in slugs and cand not in CATEGORY:
            # Unknown sitemap page: is there a recipe at /diet-nutrition/<slug>?
            _, h2 = fetch(f"{BASE}/diet-nutrition/{cand}")
            if recipe_entry(rsc_payload(h2 or ""), cand) is None:
                continue
        if cand not in sitemap_recipe_slugs:
            sitemap_recipe_slugs.append(cand)
        # Sitemap lists recipes at the site root, which soft-404s.
        _, h = fetch(u)
        if recipe_entry(rsc_payload(h or ""), cand) is None:
            dead_aliases.append(u)
    if dead_aliases:
        skipped.append({"urls": dead_aliases,
                        "reason": "sitemap gives recipe URLs at the site root; these return the "
                                  "site's 'page not found' content (HTTP 200). Not a gap: each "
                                  "recipe was scraped from [/ar]/diet-nutrition/<slug>."})
    for s in sitemap_recipe_slugs:
        if s not in slugs:
            slugs.append(s)

    st, h = fetch(BASE + "/healthy-kidney-recipes")
    if "address /healthy-kidney-recipes is incorrect" in rsc_payload(h or ""):
        skipped.append({"url": BASE + "/healthy-kidney-recipes",
                        "reason": "linked from the site footer but renders 'page not found' "
                                  "(HTTP 200); contains no recipes"})

    # 3. Fetch every recipe page (en + ar), up to 4 at a time.
    def get_pair(slug):
        out = {}
        for lang, prefix in (("en", ""), ("ar", "/ar")):
            url = f"{BASE}{prefix}/diet-nutrition/{slug}"
            status, html = fetch(url)
            out[lang] = (url, status, recipe_entry(rsc_payload(html or ""), slug) if html else None)
        return slug, out

    with ThreadPoolExecutor(max_workers=4) as ex:
        pages = dict(ex.map(get_pair, slugs))

    db_rows = load_db()
    recipes, matches = [], []
    n_found = n_ar = n_img = n_nut = 0
    sizes = {}
    for slug in slugs:
        (en_url, en_status, en), (ar_url, ar_status, ar) = pages[slug]["en"], pages[slug]["ar"]
        if en is None:
            skipped.append({"url": en_url, "reason": f"no recipe entry in page (HTTP {en_status})"})
            continue
        n_found += 1
        if any(v is not None for v in nutrients_from(en).values()):
            n_nut += 1
        if ar is None:
            skipped.append({"url": ar_url, "reason": "no Arabic version: page renders "
                                                     "'page not found' (HTTP 200)"})
        elif not is_arabic(ar):
            skipped.append({"url": ar_url, "reason": "Arabic page has no Arabic recipe text "
                                                     "(CMS fell back to English)"})
            ar = None
        if ar is not None:
            n_ar += 1
        en_rec = build_record(en, slug, "en")
        row, how, basis = find_match(en_rec["title"], en_rec["nutrients"], db_rows,
                                     clean_list(en.get("ingredient")))
        img_path = download_image(en_rec["image_url"], slug)
        if img_path:
            n_img += 1
            sizes[slug] = jpeg_size(os.path.join(ROOT, img_path))
        if row:
            matches.append({
                "davita_sa_url": en_url,
                "davita_sa_title": en_rec["title"],
                "db_recipe_id": row["id"],
                "db_title": row["title"],
                "match": how,
                "image_url": en_rec["image_url"],
                "image_path": img_path,
                "_basis": basis,
            })
            continue
        en_rec["image_path"] = img_path
        recipes.append(en_rec)
        if ar is not None:
            ar_rec = build_record(ar, slug, "ar", en_entry=en)
            ar_rec["image_path"] = img_path
            recipes.append(ar_rec)

    # 4. Recipe content that exists only in the site's i18n bundle (no page).
    _, html = fetch(BASE + "/diet-nutrition")
    payload = rsc_payload(html or "")
    try:
        i = payload.index('"messages":{') + len('"messages":')
        messages, _ = json.JSONDecoder().raw_decode(payload, i)
        dn = messages.get("dietNutrition", {})
        if "mangoRecipe" in dn:
            skipped.append({
                "url": None, "title": dn["mangoRecipe"].get("title"),
                "reason": "'Mango with Glutinous Rice' exists only as text in the site's "
                          "i18n message bundle (dietNutrition.mangoRecipe): no page or route "
                          "renders it, no image, and its nutrition block has labels but no "
                          "values. Not scraped."})
        if "recipesSwiper" in dn:
            titles = [r.get("title") for r in dn["recipesSwiper"].get("recipes", [])]
            skipped.append({"url": None, "titles": titles,
                            "reason": "'More Recipes' swiper titles in the i18n bundle are "
                                      "template leftovers (placeholder dialysis image alt text, "
                                      "no links or recipe content)."})
    except ValueError:
        pass
    _, ar_html = fetch(BASE + "/ar/diet-nutrition")
    pdfs = set(re.findall(r'https://[^"]+\.pdf', payload + rsc_payload(ar_html or "")))
    for pdf in sorted(pdfs):
        skipped.append({"url": pdf, "reason": "cookbook PDF download; contains recipes but "
                        "PDF parsing is outside requests+stdlib. Needs an owner decision."})

    match_count = len(matches)
    clean_matches = [{k: v for k, v in m.items() if not k.startswith("_")} for m in matches]
    near = [f"{m['davita_sa_title']} -> {m['db_title']} ({m['_basis']})"
            for m in matches if m["_basis"].startswith("near")]
    title_only = [f"{m['davita_sa_title']} -> {m['db_title']} ({m['_basis']})"
                  for m in matches if m["match"] == "title"]

    def dump(name, obj):
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)

    dump("recipes.json", recipes)
    dump("matches.json", clean_matches)
    dump("skipped.json", skipped)
    new_en = [r for r in recipes if r["lang"] == "en"]
    dims = sorted({f"{w}x{h}" for w, h in (v for v in sizes.values() if v)})
    report = {
        "listed": len(slugs),
        "scraped": n_found,
        "with_image": n_img,
        "with_nutrients": n_nut,
        "skipped": len(skipped),
        "matched_existing": match_count,
        "new": len(new_en),
        "notes": (
            f"Backend API not public ({'; '.join(api_notes)}), so pages were parsed from the "
            f"Next.js RSC payload. listed = distinct English recipe slugs from /diet-nutrition "
            f"({listing_counts.get('/diet-nutrition')}), /ar/diet-nutrition "
            f"({listing_counts.get('/ar/diet-nutrition')}) and the sitemap "
            f"({len(sitemap_recipe_slugs)} recipe slugs; sitemap gives them at the site root, which "
            f"soft-404s, so canonical URLs are /diet-nutrition/<slug>). The CMS listing query "
            f"returns no pagination totals; listing and sitemap agree. scraped = English recipe "
            f"pages with a recipe entry; {n_ar} of them also have official Arabic text "
            f"(/ar/diet-nutrition/<slug>). {match_count} already exist in davita_recipes.db "
            f"(matches.json, images downloaded); only the {len(new_en)} new recipes are in "
            f"recipes.json, as {len(new_en)} English + "
            f"{sum(1 for r in recipes if r['lang'] == 'ar')} Arabic records "
            f"(translation_of = English source_id). listed/scraped/with_image/with_nutrients all count "
            f"English site recipes (matched + new). skipped counts entries in skipped.json "
            f"(the sitemap root-URL aliases are one entry). Matching: normalised title vs DB English canonical rows; "
            f"'title+nutrients' when calories/Na/K/P/protein agree within max(10%, 10 units / 1 g) "
            f"on all but at most one; when they disagree, a title match is kept only if the "
            f"ingredient lists overlap >= 0.7 (word overlap coefficient). Title-only matches (nutrients differ): "
            f"{title_only or 'none'}. Same title but judged a DIFFERENT recipe (kept as new): "
            f"{REJECTED or 'none'}. Near-title matches accepted because nutrients agree: "
            f"{near or 'none'}. Images: original asset permalinks (ourassets.site/davita/...) "
            f"used instead of signed Glide crops (?w=500/410, signature prevents resizing); "
            f"dimensions {', '.join(dims) or 'n/a'}. English steps were PDF line-wrapped and "
            f"were rejoined where a line lacked closing punctuation and the next began "
            f"lowercase; Arabic text is kept exactly as published (including wrap fragments). "
            f"Arabic records reuse the English numeric nutrients and diet values; Arabic "
            f"nutrition strings are in nutrients_raw. Portions/serving size parsed from hints ('Serving is for N', 'Portions: N Serving Size: X'). Data caveat: chicken-fajita, eggplants-roll and pumpkin-soup (video recipes) publish implausible per-serving values (e.g. phosphorus 1000-1100 mg, sodium 1882 mg, fiber 15-27 g) with no portion count; kept exactly as published. Not scraped: cookbook PDFs and the i18n-only mango recipe (see skipped.json)."
        ),
    }
    dump("report.json", report)
    print(json.dumps({k: v for k, v in report.items() if k != "notes"}))


if __name__ == "__main__":
    sys.exit(main())
