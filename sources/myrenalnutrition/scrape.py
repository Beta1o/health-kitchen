#!/usr/bin/env python3
"""Scraper for My Renal Nutrition recipes (https://www.myrenalnutrition.com/recipes).

Discovery: the /recipes listing pager (?page=N) plus the four category filters
(field_recipe_category_target_id=204..207) which also give each recipe's site
category. The sitemap.xml contains no recipe URLs (checked and reported).
Re-runnable: raw pages are cached under cache/, images are not re-downloaded.
"""
import html
import json
import os
import re
import sys
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

import requests

KEY = "myrenalnutrition"
SOURCE_NAME = "My Renal Nutrition"
BASE = "https://www.myrenalnutrition.com"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
IMAGES = os.path.join(HERE, "images")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
DISALLOWED = ("/core/", "/profiles/", "/admin/", "/search/", "/user/", "/node/add/",
              "/comment/reply/", "/filter/tips", "/index.php/")
SITE_CATS = {"204": "Meal Ideas", "205": "Drink Ideas", "206": "Dessert Ideas", "207": "First Foods"}

session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"})


def allowed(url):
    path = url.replace(BASE, "")
    return not any(path.startswith(d) for d in DISALLOWED)


def fetch(url, binary=False, cache=True):
    """GET with retry/backoff. Text responses are cached under cache/."""
    assert allowed(url), url
    cpath = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest() + ".html")
    if cache and not binary and os.path.exists(cpath):
        with open(cpath, encoding="utf-8") as f:
            return 200, f.read()
    delay = 2
    last = None
    for attempt in range(6):
        try:
            r = session.get(url, timeout=60)
            last = r.status_code
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(delay); delay *= 2; continue
            if r.status_code != 200:
                return r.status_code, None
            if binary:
                return 200, r
            text = r.text
            if cache:
                os.makedirs(CACHE, exist_ok=True)
                with open(cpath, "w", encoding="utf-8") as f:
                    f.write(text)
            return 200, text
        except requests.RequestException as e:
            last = str(e)
            time.sleep(delay); delay *= 2
    return last, None


def clean(s):
    if s is None:
        return None
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


# ---------------------------------------------------------------- discovery
CARD_RE = re.compile(
    r'<div class="block--recipe-item[^"]*" style="--recipe-category-color: (#\w+)">.*?'
    r'href="(/recipes/[^"]+)".*?background-image:url\(\'([^\']*)\'\)', re.S)


def walk_listing(query):
    """Follow a listing's pager until a page yields no new cards."""
    found = {}
    page = 0
    while page < 100:
        url = f"{BASE}/recipes?{query}page={page}"
        st, h = fetch(url)
        if not h:
            break
        cards = CARD_RE.findall(h)
        new = [c for c in cards if c[1] not in found]
        if not cards or not new:
            break
        for color, href, img in cards:
            found.setdefault(href, {"color": color, "card_image": img})
        pages = [int(x) for x in re.findall(r'[?&;]page=(\d+)', h)]
        if not pages or page >= max(pages):
            break
        page += 1
    return found


def discover():
    listing = walk_listing("")
    site_cat = {}
    for cid, name in SITE_CATS.items():
        for href in walk_listing(f"field_recipe_category_target_id={cid}&"):
            site_cat[href] = name
    st, sm = fetch(BASE + "/sitemap.xml")
    sitemap_recipes = sorted(set(re.findall(r"<loc>(https?://[^<]*/recipes/[^<]+)</loc>", sm or "")))
    return listing, site_cat, sitemap_recipes


# ---------------------------------------------------------------- parsing
NUT_ROWS = [
    (r"^(calories|energy)", "calories"),
    (r"^protein", "protein_g"),
    (r"^sodium", "sodium_mg"),
    (r"^potassium", "potassium_mg"),
    (r"^phosph", "phosphorus_mg"),
    (r"^calcium", "calcium_mg"),
    (r"^(carbohydrate|carbs)", "carbohydrates_g"),
    (r"^fat", "fat_g"),
    (r"^fib", "fiber_g"),
    (r"^cholesterol", "cholesterol_mg"),
]
MMOL = {"sodium_mg": 23, "potassium_mg": 39.1, "phosphorus_mg": 31}


def num(s):
    return float(s) if "." in s else int(s)


def parse_value(field, cell):
    t = cell.replace(",", "")
    m = re.search(r"(\d+(?:\.\d+)?)\s*mg", t)
    if field.endswith("_mg") and m:
        return num(m.group(1))
    m = re.search(r"(\d+(?:\.\d+)?)\s*mmol", t)
    if field.endswith("_mg") and m and not re.search(r"\d\s*/", t):
        f = MMOL.get(field)
        return round(num(m.group(1)) * f) if f else None
    m = re.search(r"\d+(?:\.\d+)?", t)
    return num(m.group(0)) if m else None


def table_rows(t):
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
        cells = [re.sub(r"<br\s*/?>", " | ", c, flags=re.I) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.S)]
        rows.append([clean(c) or "" for c in cells])
    return rows


def parse_nutrition(block):
    m = re.search(r"<table.*?</table>", block or "", re.S)
    if not m:
        return None, None, None
    rows = table_rows(m.group(0))
    if not rows or not any(re.search(r"\d", c) for r in rows for c in r[1:]):
        return None, None, None
    raw = "; ".join(" ".join(c for c in r if c) for r in rows if any(r))
    header, body = rows[0], rows[1:]
    ncol = max(len(r) for r in rows)
    # unit column: body cells without digits but with unit words
    unit_cols = set()
    for ci in range(1, ncol):
        vals = [r[ci] for r in body if ci < len(r) and r[ci]]
        if vals and all(not re.search(r"\d", v) for v in vals):
            unit_cols.add(ci)
    value_cols = [ci for ci in range(1, ncol) if ci not in unit_cols]
    col, label = None, None
    for ci in value_cols:
        h = header[ci] if ci < len(header) else ""
        if not re.match(r"(?i)\s*per\s*100\s*(g|ml)\s*$", h):
            col, label = ci, h
            break
    if col is None:
        return None, raw, None  # only per-100 data
    if not label and header and re.match(r"(?i)per ", header[0] or ""):
        label = header[0]
    # serving size from column header
    serving = None
    if label:
        lab = re.sub(r"\s+", " ", label).strip()
        lab = re.sub(r"\(\s*", "(", re.sub(r"\s*\)", ")", lab))
        mm = re.match(r"(?i)per portion\s*\((.+)\)$", lab)
        if mm:
            serving = mm.group(1)
        elif re.match(r"(?i)per portion\s*-\s*(.+)$", lab):
            serving = re.match(r"(?i)per portion\s*-\s*(.+)$", lab).group(1)
        elif re.match(r"(?i)per (?!portion)(.+)$", lab):
            serving = re.match(r"(?i)per (.+)$", lab).group(1)
            if not re.match(r"\d", serving):
                serving = "1 " + serving
    nutrients = {k: None for k in ["calories", "protein_g", "carbohydrates_g", "fat_g", "cholesterol_mg",
                                   "sodium_mg", "potassium_mg", "phosphorus_mg", "calcium_mg", "fiber_g",
                                   "added_sugar_g"]}
    seen_data = False
    for r in body:
        name = r[0] if r else ""
        cell = r[col] if col < len(r) else ""
        if not re.search(r"\d", cell):
            if seen_data and name:  # a second labelled section (e.g. "per serving of sauce")
                break
            continue
        for pat, field in NUT_ROWS:
            if re.search(pat, name, re.I):
                if nutrients[field] is None:
                    nutrients[field] = parse_value(field, cell)
                seen_data = True
                break
    if not any(v is not None for v in nutrients.values()):
        return None, raw, serving
    return nutrients, raw, serving


def section(h, cls):
    m = re.search(r'<div class="' + re.escape(cls) + r'">(.*?)(?=<div class="ren_rec--(?:method|other|video_wrapper|file_wrapper|ingredients)"|<div class="ren_rec-row ren_rec--other|$)', h, re.S)
    return m.group(1) if m else ""


def parse_ingredients(h):
    m = re.search(r'<ul class="ren_rec--ingredients--list">(.*?)</ul>', h, re.S)
    out, group = [], None
    if not m:
        return out
    for li in re.findall(r"<li[^>]*>(.*?)</li>", m.group(1), re.S):
        txt = clean(li)
        if not txt:
            continue
        if re.fullmatch(r"\s*<(strong|b|h\d)[^>]*>.*?</\1>\s*", li, re.S) or re.fullmatch(r".{1,60}:", txt):
            group = txt.rstrip(":").strip()
            continue
        out.append([group, txt])
    return out


def parse_steps(h):
    m = re.search(r'<ol class="ren_rec--method--list">(.*?)</ol>\s*</div>', h, re.S)
    out, group = [], None
    if not m:
        return out
    for li in re.findall(r"<li>(.*?)</li>", m.group(1), re.S):
        hm = re.search(r"<h\d[^>]*>(.*?)</h\d>", li, re.S)
        if hm:
            group = (clean(hm.group(1)) or "").rstrip(":").strip() or None
            li = li.replace(hm.group(0), "")
        # a leading bold paragraph (or bold line ended by <br>) is a sub-heading
        bm = re.match(r"\s*(?:<div>)?\s*<p>\s*<(strong|b)>(.*?)</\1>\s*(?:&nbsp;|\s)*(</p>|<br\s*/?>)", li, re.S)
        if bm:
            group = (clean(bm.group(2)) or "").rstrip(":").strip() or None
            li = li[:bm.start(1) - 1] + ("<p>" if bm.group(3).startswith("<br") else "") + li[bm.end():]
        txt = clean(li)
        if txt:
            out.append([group, txt])
    return out


def parse_hints(h):
    hints = []
    for m in re.finditer(r'<div class="ren_rec--hint--inner">(.*?)</div>', h, re.S):
        for p in re.findall(r"<(?:p|li)[^>]*>(.*?)</(?:p|li)>", m.group(1), re.S) or [m.group(1)]:
            t = clean(p)
            if t:
                hints.append([None, t])
    m = re.search(r'<div class="ren_rec--renastep_text">(.*?)</div>', h, re.S)
    if m:
        for p in re.findall(r"<p[^>]*>(.*?)</p>", m.group(1), re.S) or [m.group(1)]:
            t = clean(p)
            if t:
                hints.append(["Renastep note", t])
    return hints


def norm_time(t):
    if t is None:
        return None
    t = t.strip()
    if not t or t.lower() in ("none", "n/a", "-"):
        return None
    return t


MEAL_CATS = {
    "Soups & Stews": ["soup", "borscht", "stew"],
    "Fish & Seafood": ["fish"],
    "Chicken & Turkey": ["chicken", "rice-bukhari", "hunkar-begendi"],
    "Beef, Lamb & Pork": ["beef", "toad-hole", "bolognese", "meatball", "golabki"],
    "Pizza & Sandwiches": ["pizza", "burger", "tacos", "gozleme"],
    "Pasta, Rice & Grains": ["pasta", "risotto", "macaroni", "burrito", "idli", "pierogi"],
    "Breads": ["bialys", "simit", "muffins", "bun"],
    "Breakfast & Brunch": ["porridge", "pancake", "egg-muffins", "cheela"],
    "Appetizers & Snacks": ["fritters", "falafel", "sambusa", "borek", "tikki", "croquettes", "polenta-chips",
                            "baba-ganoush", "pasty", "wedges", "popcorn", "cig-kofte", "nuggets"],
    "Vegetables": ["cauliflower", "puree", "nut-roast", "tofu", "paneer"],
}


# explicit fixes where the site category + keywords give the wrong best fit
OVERRIDES = {
    "baklava": "Desserts",
    "maida-peda": "Desserts",
    "borek": "Appetizers & Snacks",
    "apple-porridge-blueberry-compote": "Breakfast & Brunch",
    "pancakes": "Breakfast & Brunch",
}


def pick_category(slug, site_cat, title):
    s = slug.lower()
    if site_cat == "Drink Ideas":
        return "Beverages"
    if site_cat == "First Foods":
        return "Desserts" if re.search(r"apple|pear|berry|banana|mango|peach", s) else "Vegetables"
    if s in OVERRIDES:
        return OVERRIDES[s]
    order = ["Breakfast & Brunch", "Soups & Stews", "Fish & Seafood", "Chicken & Turkey", "Beef, Lamb & Pork",
             "Pizza & Sandwiches", "Pasta, Rice & Grains", "Breads", "Appetizers & Snacks", "Vegetables"]
    if site_cat == "Dessert Ideas":
        if any(k in s for k in ["bialys", "simit", "bun"]):
            return "Breads"
        if any(k in s for k in ["popcorn"]):
            return "Appetizers & Snacks"
        return "Desserts"
    for cat in order:
        if any(k in s for k in MEAL_CATS[cat]):
            return cat
    return "Vegetables"


def video_url(h):
    m = re.search(r'<iframe[^>]+src="([^"]+)"', h)
    if not m:
        return None
    src = html.unescape(m.group(1))
    y = re.search(r"youtube(?:-nocookie)?\.com/embed/([\w-]+)", src)
    if y:
        return "https://www.youtube.com/watch?v=" + y.group(1)
    v = re.search(r"player\.vimeo\.com/video/(\d+)", src)
    if v:
        return "https://vimeo.com/" + v.group(1)
    return urljoin(BASE, src)


def parse_recipe(slug_path, h, card, site_cat):
    slug = slug_path.rsplit("/", 1)[-1]
    rec_start = h.find('class="ren_rec"')
    if rec_start < 0:
        return None
    body = h[rec_start:h.find("ren_rec--back_link_wrapper", rec_start)]
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    title = clean(re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S).group(1))
    desc = re.search(r'<meta name="description" content="([^"]*)"', h)
    desc = clean(desc.group(1)) if desc else None
    img = re.search(r'ren_rec--header--img_wrapper">\s*<img src="([^"]+)"', body, re.S)
    image_url = urljoin(BASE, img.group(1)) if img else (urljoin(BASE, card["card_image"]) if card.get("card_image") else None)

    base = {}
    for item in re.findall(r'ren_rec--base_info--item">\s*(.*?)\s*</li>', body, re.S):
        t = clean(item) or ""
        for part in t.split("|"):
            if ":" in part:
                k, v = part.split(":", 1)
                base.setdefault(k.strip().lower(), v.strip())
    portions = base.get("makes")
    if portions:
        portions = re.sub(r"\s+", " ", portions).strip()
        pm = re.fullmatch(r"(?i)(\d+(?:\s*-\s*\d+)?)\s*(portions?|servings?)", portions)
        if pm:
            portions = pm.group(1).replace(" ", "")
        portions = portions or None
    cook = base.get("cooking time")
    if "chilling time" in base:
        cook = "; ".join(x for x in [norm_time(cook), "Chilling time: " + base["chilling time"]] if x)

    nut_block = re.search(r'<div class="ren_rec--nutrition">(.*?)</table>', body, re.S)
    nutrients, raw, serving = parse_nutrition(nut_block.group(0) + "</table>" if nut_block else "")
    hints = parse_hints(body)
    vt = re.search(r'ren_rec--video--text">\s*(.*?)\s*</div>', body, re.S)

    text_blob = " ".join(filter(None, [title, desc, clean(vt.group(1)) if vt else None,
                                       " ".join(t for _, t in hints)])).lower()
    diet = []
    if re.search(r"\bvegetarian\b", text_blob) or re.search(r'title="[^"]*vegetarian', body, re.I):
        diet.append("Vegetarian")
    if re.search(r"\bgluten[- ]free\b", text_blob):
        diet.append("Gluten-free")

    return {
        "source": KEY,
        "source_name": SOURCE_NAME,
        "source_id": slug,
        "url": canon.group(1) if canon else BASE + slug_path,
        "lang": "en",
        "title": title,
        "description": desc,
        "image_url": image_url,
        "image_path": None,
        "portions": portions,
        "serving_size": serving,
        "category": pick_category(slug, site_cat, title),
        "diet": diet,
        "dish": [], "cuisine": [], "method": [],
        "nutrients": nutrients,
        "nutrients_raw": raw,
        "ingredients": parse_ingredients(body),
        "steps": parse_steps(body),
        "hints": hints,
        "food_choices": [],
        "carb_choices": None,
        "video_url": video_url(body),
        "prep_time": norm_time(base.get("preparation time")),
        "cook_time": norm_time(cook),
        "total_time": None,
        "translation_of": None,
        "_site_category": site_cat,
    }


def download_image(rec):
    url = rec["image_url"]
    if not url:
        return
    ext = os.path.splitext(url.split("?")[0])[1].lower() or ".jpg"
    if ext == ".jpeg":
        ext = ".jpg"
    fname = rec["source_id"] + ext
    path = os.path.join(IMAGES, fname)
    rel = f"sources/{KEY}/images/{fname}"
    if os.path.exists(path) and os.path.getsize(path) > 0:
        rec["image_path"] = rel
        return
    st, r = fetch(url, binary=True)
    if st == 200 and r is not None and r.content:
        # write directly (os.replace on /mnt/c can hit Windows file locks)
        try:
            with open(path, "wb") as f:
                f.write(r.content)
            if os.path.getsize(path) == len(r.content):
                rec["image_path"] = rel
        except OSError as e:
            print("image write failed", fname, e)


def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(IMAGES, exist_ok=True)
    listing, site_cat, sitemap_recipes = discover()
    print(f"listing: {len(listing)} recipes; category filters: {len(site_cat)}; sitemap recipe URLs: {len(sitemap_recipes)}")
    for u in sitemap_recipes:
        p = u.replace(BASE, "")
        listing.setdefault(p, {"color": None, "card_image": None})

    skipped, recipes = [], []

    def work(href):
        url = BASE + href
        if not allowed(url):
            return href, None, "disallowed by robots.txt"
        st, h = fetch(url)
        if not h:
            return href, None, f"HTTP {st}"
        try:
            rec = parse_recipe(href, h, listing[href], site_cat.get(href))
        except Exception as e:  # keep going; report it
            return href, None, f"parse error: {e!r}"
        if not rec:
            return href, None, "no recipe content (possible block page)"
        return href, rec, None

    with ThreadPoolExecutor(max_workers=3) as ex:
        results = list(ex.map(work, sorted(listing)))
    for href, rec, err in results:
        if err:
            skipped.append({"url": BASE + href, "reason": err})
        else:
            recipes.append(rec)

    with ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(download_image, recipes))

    for r in recipes:
        r.pop("_site_category", None)
    recipes.sort(key=lambda r: r["source_id"])
    with open(os.path.join(HERE, "recipes.json"), "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)
    with open(os.path.join(HERE, "skipped.json"), "w", encoding="utf-8") as f:
        json.dump(skipped, f, ensure_ascii=False, indent=2)

    with_img = sum(1 for r in recipes if r["image_path"])
    with_nut = sum(1 for r in recipes if r["nutrients"] and any(v is not None for v in r["nutrients"].values()))
    no_nut = [r["source_id"] for r in recipes if not r["nutrients"]]
    notes = (
        f"Recipes found via the /recipes listing pager (?page=0..N); {len(listing)} unique slugs, cross-checked "
        f"against the 4 site category filters (Meal/Drink/Dessert/First Foods) = {len(site_cat)}. "
        f"sitemap.xml lists {len(sitemap_recipes)} recipe URLs (it only covers info pages). "
        f"image = recipe-page header photo (cut-out PNG/WebP with transparent background); the listing-card "
        f"originals are multi-MB AdobeStock files so were not used. Nutrients taken from the per-portion column "
        f"(mg values; mmol only when no mg given). No nutrition given for: {', '.join(no_nut) or 'none'}. "
        f"Values kept as published (e.g. fish-fingers lists 20 kcal per portion; christmas-tree protein is "
        f"labelled kcal on site, taken as g). bean-burger table also has a per-sauce section, kept in "
        f"nutrients_raw only. Most recipes use Renastep (Vitaflo); its medical-supervision note is kept as a hint. "
        f"Category mapped from site category + slug keywords."
    )
    report = {"listed": len(listing), "scraped": len(recipes), "with_image": with_img,
              "with_nutrients": with_nut, "skipped": len(skipped), "notes": notes}
    with open(os.path.join(HERE, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    sys.exit(main())
