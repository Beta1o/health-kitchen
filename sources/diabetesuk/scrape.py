#!/usr/bin/env python3
"""Scrape every recipe published by Diabetes UK.

Discovery: the recipe landing listing (all pages), the same listing under every
filter value (special diets, meals & courses, main ingredient; all pages), and the
XML sitemap. The filter memberships are also used for category/diet/dish mapping.
Output follows sources/FORMAT.md. Re-runnable: raw pages are cached under cache/
and images already on disk are not re-downloaded.

robots.txt: crawl-delay 5, so one request every 5+ seconds; the filter form action
(/guide-to-diabetes/recipes/recipe-search-results) and any ?search= URL are
disallowed and never requested -- filters are applied to the landing page URL.
Set DUK_FRESH_LISTING=1 to refetch listing/sitemap pages instead of using cache.
"""
import hashlib
import html
import json
import math
import os
import re
import sys
import time
from urllib.parse import urljoin, urlparse, quote

import requests

KEY = "diabetesuk"
SOURCE_NAME = "Diabetes UK"
BASE = "https://www.diabetes.org.uk"
LANDING = BASE + "/living-with-diabetes/eating/recipes"
SITEMAP = BASE + "/sitemap.xml"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
IMAGES = os.path.join(HERE, "images")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
MAX_KEEP = 1024 * 1024       # re-download (as the 772px derivative) anything larger
MIN_INTERVAL = 5.5          # robots.txt crawl-delay: 5
FRESH_LISTING = os.environ.get("DUK_FRESH_LISTING") == "1"
_last = [0.0]
_blocked = [0]
BLOCK_LIMIT = 5

session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"})

RECIPE_PATH_RE = re.compile(
    r"^/(?:guide-to-diabetes/recipes|living-with-diabetes/eating/recipes|"
    r"living-with-diabetes/recipes)/([a-z0-9][a-z0-9-]*)/?$")
ROBOTS_DISALLOW = ("/core", "/profiles", "/admin", "/documents", "/resources",
                   "/upload", "/user/", "/node/add", "/comment/reply", "/filter/tips",
                   "/guide-to-diabetes/recipes/recipe-search-results", "/index.php")

FILTERS = {
    "special_diets": {"44": "Dairy free", "45": "Freezer safe", "46": "Gluten free",
                      "47": "Low fat", "48": "Low sugar", "49": "Nut free",
                      "50": "Vegan", "51": "Vegetarian"},
    "meals_courses": {"33": "Party food", "30": "Side dish / Starter", "31": "Snack",
                      "29": "Main meal", "173": "Celebrations", "32": "Baking and dessert",
                      "28": "Breakfast", "34": "Asian recipes"},
    "main_ingredient": {"35": "Beef", "36": "Chicken", "39": "Fish & Seafood",
                        "41": "Fruit", "38": "Lamb", "42": "Pasta", "37": "Pork",
                        "43": "Rice", "40": "Vegetables"},
}


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def robots_ok(url):
    p = urlparse(url)
    path = p.path
    if any(path.startswith(d) for d in ROBOTS_DISALLOW):
        return False
    q = p.query
    if any(k in q for k in ("search=", "region=", "subject=", "research_area=")):
        return False
    return "views/ajax" not in url


def is_challenge(text):
    t = text[:20000].lower()
    return ("just a moment" in t and "cf-" in t) or "cf-chl" in t or \
        "challenge-platform" in t or "captcha" in t and "<form" in t and "recipe" not in t


class Blocked(Exception):
    pass


def fetch(url, binary=False, use_cache=True):
    """Return (status, body). Caches successful text pages. Raises Blocked."""
    path = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest() + ".html")
    if use_cache and not binary and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return 200, f.read()
    if not robots_ok(url):
        log("  robots.txt disallows", url)
        return -2, None
    if _blocked[0] >= BLOCK_LIMIT:
        raise Blocked(url)
    delay = 10
    for attempt in range(6):
        wait = _last[0] + MIN_INTERVAL - time.time()
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = session.get(url, timeout=60)
        except requests.RequestException as e:
            log("  err", url, e)
            time.sleep(delay)
            delay *= 2
            continue
        if r.status_code == 429 or r.status_code >= 500:
            ra = r.headers.get("Retry-After")
            log("  retry", r.status_code, url)
            time.sleep(int(ra) if ra and ra.isdigit() else delay)
            delay *= 2
            continue
        if r.status_code == 403 or (not binary and is_challenge(r.text)):
            _blocked[0] += 1
            log("  BLOCKED/challenge", r.status_code, url)
            time.sleep(60 * _blocked[0])   # slow down
            if _blocked[0] >= BLOCK_LIMIT:
                raise Blocked(url)
            continue
        _blocked[0] = 0
        if r.status_code != 200:
            return r.status_code, None
        if binary:
            return 200, r.content
        text = r.text
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return 200, text
    return -1, None


# ---------------------------------------------------------------- helpers
def clean(s):
    if s is None:
        return None
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s).replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,.;:!?)])", r"\1", s)
    s = re.sub(r"\(\s+", "(", s)
    return s or None


def strip_noise(s):
    s = re.sub(r"<script\b.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<style\b.*?</style>", "", s, flags=re.S)
    s = re.sub(r"<svg\b.*?</svg>", "", s, flags=re.S)
    return s


def paras(fragment):
    out = []
    for _, t in re.findall(r"<(p|li|h[2-6])\b[^>]*>(.*?)</\1>", fragment, re.S):
        t = clean(t)
        if t:
            out.append(t)
    if not out:
        t = clean(fragment)
        if t:
            out = [t]
    return out


def num(s):
    if s is None:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", s.replace(",", ""))
    return float(m.group(1)) if m else None


def rnd(x, nd=1):
    if x is None:
        return None
    v = round(x, nd)
    return int(v) if v == int(v) else v


def norm_url(href):
    u = urljoin(BASE + "/", html.unescape(href))
    p = urlparse(u)
    if p.netloc not in ("www.diabetes.org.uk", "diabetes.org.uk"):
        return None
    m = RECIPE_PATH_RE.match(p.path)
    if not m:
        return None
    return BASE + p.path.rstrip("/")


def slug_of(url):
    return url.rstrip("/").rsplit("/", 1)[-1]


# ---------------------------------------------------------------- listings
CARD_RE = re.compile(r'<article class="card recipes-card">(.*?)</article>', re.S)


def parse_listing(text):
    """Return (shown_count, [(url, title, [diet icons])])."""
    m = re.search(r"Showing<span[^>]*>\s*(\d+)\s*</span>", text)
    shown = int(m.group(1)) if m else None
    cards = []
    for c in CARD_RE.findall(text):
        a = re.search(r'<a href="([^"]+)"[^>]*itemprop="url"', c) or \
            re.search(r'<h3>\s*<a href="([^"]+)"', c)
        if not a:
            continue
        url = norm_url(a.group(1))
        if not url:
            log("  unexpected card link", a.group(1))
            continue
        t = re.search(r"<span>(.*?)</span>", c, re.S)
        icons = re.findall(r'special_diets_icon/[^"]*"\s+alt="([^"]*)"', c)
        cards.append((url, clean(t.group(1)) if t else None, icons))
    return shown, cards


def crawl_listing(qs=""):
    """Crawl all pages of the landing listing with optional filter query string."""
    found, shown, page = [], None, 0
    seen = set()
    while True:
        q = (qs + "&" if qs else "") + "page=%d" % page
        url = LANDING + "?" + q
        st, text = fetch(url, use_cache=not FRESH_LISTING)
        if st != 200:
            log("  listing failed", st, url)
            break
        s, cards = parse_listing(text)
        if shown is None:
            shown = s
        new = [c for c in cards if c[0] not in seen]
        if not new:
            break
        for c in new:
            seen.add(c[0])
            found.append(c)
        if shown is not None and len(seen) >= shown:
            break
        page += 1
        if page > 200:
            break
    return shown, found


def crawl_sitemap():
    urls = []
    st, idx = fetch(SITEMAP, use_cache=not FRESH_LISTING)
    subs = re.findall(r"<loc>([^<]+)</loc>", idx or "")
    if not re.search(r"<sitemapindex", idx or ""):
        subs = [SITEMAP]
    for sm in subs:
        sm = html.unescape(sm)
        st, x = fetch(sm, use_cache=not FRESH_LISTING)
        for loc in re.findall(r"<loc>([^<]+)</loc>", x or ""):
            u = norm_url(loc.strip())
            if u:
                urls.append(u)
    return urls


# ---------------------------------------------------------------- recipe page
def jsonld_recipe(text):
    for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            d = json.loads(blob)
        except ValueError:
            try:
                d = json.loads(re.sub(r",\s*([\]}])", r"\1", blob))
            except ValueError:
                continue
        items = d if isinstance(d, list) else d.get("@graph", [d]) if isinstance(d, dict) else []
        for it in items:
            if isinstance(it, dict) and it.get("@type") in ("Recipe", ["Recipe"]):
                return it
    return None


def section(text, start_pat, end_pat):
    m = re.search(start_pat, text, re.S)
    if not m:
        return None
    rest = text[m.end():]
    e = re.search(end_pat, rest, re.S)
    return rest[: e.start()] if e else rest


def parse_time_block(card, label):
    m = re.search(r"<div>\s*%s\s*</div>\s*<(?:meta|span)[^>]*>(.*?)</(?:meta|span)>" % label,
                  card, re.S | re.I)
    if not m:
        return None
    v = clean(m.group(1))
    if not v or v.lower().startswith("see below") or not re.search(r"\d", v):
        return None
    return v


NUT_MAP = {"kcal": "calories", "calories": "calories", "energy": "calories",
           "carbs": "carbohydrates_g", "carbohydrate": "carbohydrates_g",
           "carbohydrates": "carbohydrates_g",
           "fibre": "fiber_g", "fiber": "fiber_g", "protein": "protein_g",
           "fat": "fat_g", "total fat": "fat_g"}
NUT_IGNORED = {"saturates", "sugars", "salt", "fruit/veg portion", "sodium", "kj",
               "saturated fat", "sugar"}
unknown_labels = {}


def parse_nutrition(text):
    sec = section(text, r'<section\s+itemprop="nutrition"[^>]*>', r"</section>")
    if not sec:
        return None, None, None, None
    head = None
    hm = re.search(r'field--name-field-nutrition-information[^>]*>(.*?)</div>\s*</div>', sec, re.S)
    if hm:
        head = clean(re.sub(r"<h2>.*?</h2>", "", hm.group(1), flags=re.S))
    rows = []
    for lab, dd in re.findall(r'<dt class="nutrition-tag__label">(.*?)</dt>\s*'
                              r'<dd class="nutrition-tag__content">(.*?)</dd>', sec, re.S):
        lab = clean(lab)
        lvl = re.search(r'nutrition-tag__content__value">(.*?)</div>', dd, re.S)
        lvl = clean(lvl.group(1)) if lvl else None
        val = clean(re.sub(r'<div class="nutrition-tag__content__value">.*?</div>', "", dd, flags=re.S))
        rows.append((lab, val, lvl))
    return head, rows, sec, hm


def build_nutrients(head, rows, portions):
    n = {k: None for k in ("calories", "protein_g", "carbohydrates_g", "fat_g",
                           "cholesterol_mg", "sodium_mg", "potassium_mg", "phosphorus_mg",
                           "calcium_mg", "fiber_g", "added_sugar_g")}
    fruitveg = None
    if not rows:
        return n, None, None
    per_serving = True
    hl = (head or "").lower()
    if re.search(r"per\s*100\s*(g|ml)|whole recipe|per recipe|entire recipe", hl):
        per_serving = False
    raw_parts = []
    vals = {}
    for lab, val, lvl in rows:
        raw_parts.append("%s %s%s" % (lab, val or "", (" " + lvl) if lvl else ""))
        key = (lab or "").lower().strip()
        v = num(val)
        if key == "fruit/veg portion":
            fruitveg = val
            continue
        if key == "salt":
            if v is not None:
                vals["sodium_mg"] = v * 400
            continue
        if key == "sodium":
            if v is not None:
                vals["sodium_mg"] = v if "mg" in (val or "").lower() else v * 1000
            continue
        if key in ("kj",):
            continue
        if key in NUT_MAP:
            if key == "energy" and "kj" in (val or "").lower() and "kcal" not in (val or "").lower():
                continue
            if v is not None:
                vals[NUT_MAP[key]] = v
            continue
        if key in ("added sugars", "free sugars", "added sugar", "free sugar"):
            if v is not None:
                vals["added_sugar_g"] = v
            continue
        if key not in NUT_IGNORED:
            unknown_labels[lab] = unknown_labels.get(lab, 0) + 1
    raw = ((head + ": ") if head else "") + "; ".join(raw_parts)
    if per_serving:
        for k, v in vals.items():
            n[k] = rnd(v, 0 if k in ("calories", "sodium_mg") else 1)
    return n, raw, fruitveg


def parse_items(fragment, item_re):
    """Walk headings and items in order -> [(group, text)]."""
    out, group = [], None
    for m in re.finditer(r"<(h[2-6]|strong|b)\b[^>]*>(.*?)</\1>|" + item_re, fragment, re.S):
        if m.group(1):
            t = clean(m.group(2))
            if not t or t.lower() in ("ingredients", "method", "recipe tips") \
                    or re.match(r"^step \d+$", t, re.I):
                continue
            if m.group(1) in ("strong", "b"):
                continue  # inline emphasis inside an item; handled by item text
            group = t.rstrip(":")
        else:
            t = clean(m.group(m.lastindex))
            if t:
                out.append([group, t])
    return out


GROUP_RE = re.compile(r"^(for (the )?|to (serve|garnish|make|decorate|finish|top)|(cold|warm) fillings?)", re.I)


def regroup(items):
    """Turn sub-heading list items ('For the sauce:') into group labels."""
    out, group = [], None
    for g, t in items:
        if (t.endswith(":") and len(t) <= 60) or \
                (GROUP_RE.match(t) and len(t) <= 40 and not re.search(r"\d", t) and "," not in t):
            group = t.rstrip(":").strip()
            continue
        out.append([group if group is not None else g, t])
    return out


def parse_recipe(url, text):
    text = strip_noise(text)
    ld = jsonld_recipe(text)
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', text)
    canon = canon.group(1) if canon else url
    title = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
    title = clean(title.group(1)) if title else (ld or {}).get("name")
    body = section(text, r'<article about="[^"]*">', r'<dialog class="modal"|Share this Page') or text
    card = section(body, r'class="recipe-card"', r'<section\s+itemprop="nutrition"') or body
    desc = re.search(r'<div\s+class="description">(.*?)</div>', card, re.S)
    desc = clean(desc.group(1)) if desc else clean((ld or {}).get("description"))
    portions = re.search(r'instruction_serves">.*?<span>(.*?)</span>', card, re.S)
    portions = clean(portions.group(1)) if portions else (clean(str((ld or {}).get("recipeYield") or "")) or None)
    prep = parse_time_block(card, "Prep")
    cook = parse_time_block(card, "Cook")
    total = None
    for v in (prep, cook):
        if v and v.lower().startswith("total prep and cook time"):
            total = clean(v.split(":", 1)[1])
    if prep and prep.lower().startswith("total prep"):
        prep = None
    if cook and cook.lower().startswith("total prep"):
        cook = None
    ldprep = clean((ld or {}).get("prepTime") or "")
    if ldprep and ldprep.lower().startswith("total prep and cook time"):
        total = total or clean(ldprep.split(":", 1)[1])
    elif ldprep and not prep and re.search(r"\d", ldprep):
        prep = ldprep
    header_tags = []
    hdr = section(text, r'class="recipe-header"', r'<article about=')
    if hdr:
        header_tags = re.findall(r'special_diets_icon/[^"]*"\s+alt="([^"]*)"', hdr)
    if not header_tags and ld and isinstance(ld.get("keywords"), list):
        header_tags = [k.strip() for k in ld["keywords"] if isinstance(k, str)]

    head, rows, _, _ = parse_nutrition(body)
    serving_size = None
    if head:
        sm = re.search(r"Each\s+(.+?)\s+serving", head, re.I)
        if sm:
            serving_size = sm.group(1).strip()

    ing_frag = section(body, r'<details class="ingredients-tab', r"</details>") or ""
    ingredients = parse_items(ing_frag, r'<li\b[^>]*>(.*?)</li>')
    if not ingredients and ld:
        ingredients = [[None, clean(x)] for x in ld.get("recipeIngredient") or [] if clean(x)]
    ingredients = regroup(ingredients)

    meth_frag = section(body, r'<details class="method-tab', r"</details>") or ""
    tips_frag = ""
    tm = re.search(r'<div\s+class="recipe-tips[^"]*">(.*)', meth_frag, re.S)
    if tm:
        tips_frag = tm.group(1)
        meth_frag = meth_frag[: tm.start()]
    steps = []
    stepblocks = re.findall(r'<div class="large-checkbox__content">(.*?)</div>\s*</label>', meth_frag, re.S)
    if stepblocks:
        for sb in stepblocks:
            sb = re.sub(r'<h4 class="recipe-step__title">.*?</h4>', "", sb, flags=re.S)
            t = " ".join(paras(sb))
            if t:
                steps.append([None, t])
    else:
        steps = parse_items(meth_frag, r'<(?:p|li)\b[^>]*>(.*?)</(?:p|li)>')
    if not steps and ld:
        for x in ld.get("recipeInstructions") or []:
            t = clean(x if isinstance(x, str) else x.get("text") if isinstance(x, dict) else None)
            if t:
                steps.append([None, t])
    hints = []
    if tips_frag:
        fi = re.search(r'<div class="field__item">(.*)', tips_frag, re.S)
        for t in paras(fi.group(1) if fi else tips_frag):
            if t.lower() != "recipe tips":
                hints.append([None, t])
    # other labelled text fields inside the article (e.g. serving suggestions)
    extra_fields = []
    for fname, lab, inner in re.findall(
            r'field--name-(field-[a-z0-9-]+) field--label-above">\s*<div class="field__label">(.*?)</div>(.*?)</div>\s*</div>',
            body, re.S):
        if fname == "field-chefs":
            continue
        extra_fields.append(fname)
        for t in paras(inner):
            hints.append([clean(lab), t])

    img = re.search(r'<meta property="og:image" content="([^"]+)"', text)
    image_url = html.unescape(img.group(1)) if img else None
    if not image_url and ld and ld.get("image"):
        im = ld["image"]
        im = im[0] if isinstance(im, list) else im.get("url") if isinstance(im, dict) else im
        image_url = urljoin(BASE, im) if im else None
    if image_url and ("logo" in image_url.lower() and "recipe" not in image_url.lower()):
        image_url = None
    # download the 772px "recipe_desktop" derivative shown on the page; some
    # originals are multi-megabyte camera files (up to ~19 MB)
    image_dl = None
    dm = re.search(r'<source srcset="([^" ]*/styles/recipe_desktop/[^" ]+)', card)
    if dm:
        image_dl = urljoin(BASE, html.unescape(dm.group(1)))
    elif image_url:
        image_dl = image_url
    video = re.search(r'<iframe[^>]+src="([^"]*(?:youtube|vimeo)[^"]*)"', body)
    return {
        "is_recipe": ld is not None or bool(ingredients and steps),
        "canonical": canon.rstrip("/"), "title": title, "description": desc,
        "portions": portions, "serving_size": serving_size,
        "prep": prep, "cook": cook, "total": total, "tags": header_tags,
        "nut_head": head, "nut_rows": rows, "ingredients": ingredients,
        "steps": steps, "hints": hints, "image_url": image_url,
        "video_url": html.unescape(video.group(1)) if video else None,
        "image_dl": image_dl,
        "extra_fields": extra_fields,
    }


# ---------------------------------------------------------------- mapping
def kw(text, words):
    return any(re.search(r"\b%s" % w, text) for w in words)


def categorize(title, courses, mains, ingredients_text):
    t = (title or "").lower()
    if kw(t, ["soup", "stew", "chowder", "broth", "casserole", "goulash", "tagine", "hotpot",
              "gumbo", "minestrone", "gazpacho", "dhal soup", "chilli con", "ramen", "laksa"]):
        return "Soups & Stews"
    if kw(t, ["smoothie", "drink", "lassi", "shake", "juice", "tea\\b", "latte", "cocktail",
              "mocktail", "punch", "lemonade", "hot chocolate", "spritz", "cooler"]):
        return "Beverages"
    if kw(t, ["salad", "slaw", "coleslaw", "tabbouleh", "dressing\\b", "vinaigrette"]):
        return "Salads & Dressings"
    if kw(t, ["sauce", "dip\\b", "dips\\b", "salsa", "chutney", "pesto", "raita", "relish",
              "hummus", "houmous", "gravy", "marinade", "spice mix", "seasoning", "jam\\b",
              "guacamole", "tzatziki", "ketchup", "mayo", "compote", "coulis"]) \
            and not kw(t, ["with\\b", "in .* sauce", "chicken", "turkey", "beef", "lamb", "pork",
                           "meatloaf", "meatball", "sausage", "fish", "salmon", "prawn", "cod\\b",
                           "pasta", "spaghetti", "fritter", "burger", "pie\\b", "steak"]):
        return "Sauces & Seasonings"
    if kw(t, ["pizza", "sandwich", "wrap", "toastie", "burger", "panini", "bruschetta",
              "pitta", "quesadilla", "tortilla", "bagel", "taco", "burrito", "fajita",
              "flatbread pizza", "open sandwich"]) and "Breakfast" not in courses:
        return "Pizza & Sandwiches"
    if kw(t, ["bread", "loaf", "roll\\b", "rolls\\b", "scone", "muffin", "chapati", "roti",
              "naan", "focaccia", "soda bread", "flatbread", "paratha", "bun\\b", "buns\\b",
              "pancake", "crumpet", "oatcake"]) and "Breakfast" not in courses \
            and not kw(t, ["pudding", "cake"]):
        return "Breads"
    if "Breakfast" in courses or kw(t, ["porridge", "granola", "overnight oats", "muesli",
                                         "breakfast", "omelette", "frittata", "scrambled",
                                         "shakshuka", "brunch"]):
        return "Breakfast & Brunch"
    if "Baking and dessert" in courses or kw(t, ["cake", "cookie", "biscuit", "brownie",
                                                  "tart\\b", "crumble", "pudding", "cheesecake",
                                                  "mousse", "trifle", "sorbet", "ice cream",
                                                  "flapjack", "jelly", "fool\\b", "pavlova",
                                                  "meringue", "dessert", "pie\\b.*(apple|berry|cherry|fruit|pumpkin|mince)",
                                                  "truffle", "fudge", "bark\\b", "parfait",
                                                  "custard", "poached (pear|fruit)", "crème", "creme"]):
        return "Desserts"
    if any(m in mains for m in ("Beef", "Lamb", "Pork")):
        return "Beef, Lamb & Pork"
    if "Chicken" in mains:
        return "Chicken & Turkey"
    if "Fish & Seafood" in mains:
        return "Fish & Seafood"
    if any(m in mains for m in ("Pasta", "Rice")):
        return "Pasta, Rice & Grains"
    tt = t + " "
    if kw(tt, ["chicken", "turkey", "duck"]):
        return "Chicken & Turkey"
    if kw(tt, ["beef", "lamb", "pork", "steak", "mince", "sausage", "bacon", "ham\\b", "gammon",
               "meatball", "kofta", "venison", "chorizo"]):
        return "Beef, Lamb & Pork"
    if kw(tt, ["fish", "salmon", "cod\\b", "haddock", "tuna", "prawn", "mackerel", "sardine",
               "seafood", "crab", "mussel", "trout", "hake", "pollock", "sea bass", "kipper",
               "squid", "scallop", "basa", "tilapia", "plaice", "monkfish"]):
        return "Fish & Seafood"
    if kw(tt, ["pasta", "spaghetti", "penne", "lasagne", "linguine", "macaroni", "noodle",
               "rice", "risotto", "quinoa", "couscous", "bulgur", "biryani", "pilau", "pilaf",
               "paella", "orzo", "tagliatelle", "fusilli", "gnocchi", "barley", "freekeh",
               "jollof", "kedgeree"]):
        return "Pasta, Rice & Grains"
    if "Fruit" in mains and "Vegetables" not in mains:
        return "Desserts"
    if "Vegetables" in mains:
        return "Vegetables"
    if any(c in courses for c in ("Snack", "Party food", "Side dish / Starter")):
        return "Appetizers & Snacks"
    return "Vegetables"


def method_of(title, steps_text):
    t = (title or "").lower()
    m = []
    if kw(t, ["slow cooker", "slow-cooked", "slow cooked"]):
        m.append("Slow Cooker")
    if kw(t, ["grilled", "griddled", "barbecue", "bbq", "chargrilled", "kebab"]):
        m.append("Grill")
    if kw(t, ["roast"]):
        m.append("Roast")
    if kw(t, ["baked", "bake\\b", "traybake", "tray bake"]):
        m.append("Bake")
    if kw(t, ["microwave"]):
        m.append("Microwave")
    if kw(t, ["no-cook", "no cook"]):
        m.append("No Cooking")
    return m


def dish_of(title, tags):
    t = (title or "").lower()
    d = []
    if "Freezer safe" in tags:
        d.append("Freezer")
    if kw(t, ["soup", "chowder", "broth", "minestrone", "gazpacho"]):
        d.append("Soup")
    if kw(t, ["stew", "casserole", "tagine", "goulash", "hotpot"]):
        d.append("Stew")
    if kw(t, ["stir-fry", "stir fry", "stir-fried"]):
        d.append("Stir-fry")
    if kw(t, ["one-pot", "one pot", "one-pan", "one pan", "traybake", "tray bake", "sheet pan"]):
        d.append("One-Dish Meal")
    if kw(t, ["cake", "cupcake", "loaf cake"]) and not kw(t, ["fish ?cake", "crab ?cake", "pancake", "potato cake", "rice cake"]):
        d.append("Cake")
    if kw(t, ["cookie", "biscuit"]):
        d.append("Cookies")
    if kw(t, ["muffin"]):
        d.append("Muffin")
    if kw(t, ["\\bpie\\b", "pies\\b"]):
        d.append("Pie")
    if kw(t, ["bread", "loaf", "rolls?\\b", "scone", "naan", "chapati", "focaccia"]) and "Cake" not in d \
            and not kw(t, ["sauce", "pudding", "crumb"]):
        d.append("Bread")
    return d


CUISINE_KW = [("Indian", ["curry", "tikka", "masala", "dhal", "dal\\b", "biryani", "korma",
                          "pakora", "bhaji", "chapati", "raita", "tandoori", "saag", "paneer",
                          "samosa", "lassi", "chana", "aloo", "jalfrezi", "dosa", "kheer", "keema", "rogan"]),
              ("Chinese", ["chinese", "chow mein", "sweet and sour", "kung pao", "char siu", "hoisin"]),
              ("Japanese", ["japanese", "teriyaki", "sushi", "miso", "katsu", "ramen"]),
              ("Italian", ["italian", "risotto", "lasagne", "bolognese", "pizza", "pesto", "minestrone",
                           "carbonara", "arrabbiata", "focaccia", "bruschetta", "cacciatore", "tiramisu"]),
              ("Mexican", ["mexican", "fajita", "burrito", "taco", "quesadilla", "enchilada",
                           "guacamole", "chilli con carne", "nachos"]),
              ("Greek", ["greek", "tzatziki", "moussaka", "souvlaki", "spanakopita"]),
              ("Middle Eastern", ["shakshuka", "falafel", "hummus", "houmous", "tabbouleh", "fattoush",
                                  "tagine", "shawarma", "za'atar", "harissa", "kofta", "afghan", "persian"]),
              ("Caribbean", ["caribbean", "jerk", "jollof", "plantain", "ackee", "callaloo"]),
              ("Mediterranean", ["mediterranean"]),
              ("French", ["french", "ratatouille", "niçoise", "nicoise", "gratin", "provençal", "cassoulet"]),
              ("Irish", ["irish", "colcannon"]),
              ("Asian", ["thai", "vietnamese", "korean", "malaysian", "indonesian", "satay", "pad thai",
                         "laksa", "bibimbap", "nasi goreng", "asian"])]


def cuisine_of(title, courses):
    t = (title or "").lower()
    c = []
    for name, words in CUISINE_KW:
        if kw(t, words):
            c.append(name)
    if "Asian recipes" in courses and not any(x in c for x in ("Indian", "Chinese", "Japanese", "Asian")):
        c.append("Asian")
    return c


def diet_of(tags):
    d = ["Diabetes"]
    if "Gluten free" in tags:
        d.append("Gluten-free")
    if "Vegetarian" in tags or "Vegan" in tags:
        d.append("Vegetarian")
    return d


# ---------------------------------------------------------------- main
def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(IMAGES, exist_ok=True)
    blocked_note = None
    skipped = []
    try:
        # 1. landing listing
        log("listing ...")
        shown_all, cards = crawl_listing()
        listing = {}
        for u, t, icons in cards:
            listing.setdefault(u, {"title": t, "icons": icons})
        log("  landing shows", shown_all, "found", len(listing))
        # 2. filters
        memb = {}            # url -> {filter label}
        filter_counts = {}
        for fname, opts in FILTERS.items():
            for val, label in opts.items():
                qs = "%s%%5B0%%5D=%s" % (fname, val)
                shown, fc = crawl_listing(qs)
                filter_counts[label] = {"shown": shown, "found": len(fc)}
                for u, t, icons in fc:
                    memb.setdefault(u, set()).add(label)
                    if u not in listing:
                        listing.setdefault(u, {"title": t, "icons": icons, "filter_only": True})
                log("  filter", label, shown, len(fc))
        # 3. sitemap
        log("sitemap ...")
        sm_urls = sorted(set(crawl_sitemap()))
        log("  sitemap recipe-path URLs", len(sm_urls))
    except Blocked as e:
        blocked_note = "Blocked/challenged during discovery at %s" % e
        log(blocked_note)
        listing = locals().get("listing", {})
        memb = locals().get("memb", {})
        filter_counts = locals().get("filter_counts", {})
        shown_all = locals().get("shown_all")
        sm_urls = locals().get("sm_urls", [])

    landing_urls = {u for u, v in listing.items() if not v.get("filter_only")}
    filter_only = sorted(u for u, v in listing.items() if v.get("filter_only"))
    candidates = sorted(set(listing) | set(sm_urls))

    # 4. recipe pages
    parsed = {}
    for i, u in enumerate(candidates):
        if blocked_note:
            skipped.append({"url": u, "reason": "not fetched: site blocked requests"})
            continue
        try:
            st, text = fetch(u)
        except Blocked as e:
            blocked_note = "Blocked/challenged while fetching recipe pages at %s" % e
            skipped.append({"url": u, "reason": "blocked"})
            continue
        if st != 200 or not text:
            skipped.append({"url": u, "reason": "HTTP %s" % st})
            continue
        try:
            parsed[u] = parse_recipe(u, text)
        except Exception as ex:  # keep going; record the failure
            skipped.append({"url": u, "reason": "parse error: %r" % ex})
        if i % 25 == 0:
            log("  pages %d/%d" % (i + 1, len(candidates)))

    # 5. build records, dedupe by canonical URL
    recipes, non_recipes, by_canon = [], [], {}
    for u, p in parsed.items():
        if not p["is_recipe"]:
            non_recipes.append(u)
            continue
        c = p["canonical"]
        if c in by_canon:
            by_canon[c]["aliases"].append(u)
            continue
        by_canon[c] = {"p": p, "aliases": [u]}

    slug_count = {}
    for c in by_canon:
        slug_count[slug_of(c)] = slug_count.get(slug_of(c), 0) + 1

    for c, entry in sorted(by_canon.items()):
        p = entry["p"]
        labels = set()
        for a in entry["aliases"] + [c]:
            labels |= memb.get(a, set())
        tags = list(dict.fromkeys(p["tags"] + [l for l in labels if l in FILTERS["special_diets"].values()]))
        courses = [l for l in FILTERS["meals_courses"].values() if l in labels]
        mains = [l.strip() for l in FILTERS["main_ingredient"].values() if l in labels]
        sid = slug_of(c)
        if slug_count[sid] > 1:
            sid = urlparse(c).path.strip("/").replace("/", "_")
        n, raw, fruitveg = build_nutrients(p["nut_head"], p["nut_rows"], p["portions"])
        extra = []
        if tags:
            extra.append("Special diets: " + ", ".join(tags))
        if courses or mains:
            extra.append("Site categories: " + ", ".join(courses + mains))
        nutrients_raw = " | ".join([x for x in [raw] + extra if x]) or None
        hints = list(p["hints"])
        if fruitveg:
            hints.append(["Fruit/veg portions", "Fruit/veg portions per serving: %s" % fruitveg])
        ing_text = " ".join(t for _, t in p["ingredients"]).lower()
        rec = {
            "source": KEY, "source_name": SOURCE_NAME, "source_id": sid, "url": c,
            "lang": "en", "title": p["title"], "description": p["description"],
            "image_url": p["image_url"], "image_path": None,
            "portions": p["portions"], "serving_size": p["serving_size"],
            "category": categorize(p["title"], courses, mains, ing_text),
            "diet": diet_of(tags),
            "dish": dish_of(p["title"], tags),
            "cuisine": cuisine_of(p["title"], courses),
            "method": method_of(p["title"], ""),
            "nutrients": n, "nutrients_raw": nutrients_raw,
            "ingredients": p["ingredients"], "steps": p["steps"], "hints": hints,
            "food_choices": [], "carb_choices": None, "video_url": p["video_url"],
            "prep_time": p["prep"], "cook_time": p["cook"], "total_time": p["total"],
            "translation_of": None,
        }
        rec["_image_dl"] = p["image_dl"]
        recipes.append(rec)

    # 6. images
    for rec in recipes:
        iu = rec.pop("_image_dl", None) or rec["image_url"]
        if not iu:
            continue
        ext = os.path.splitext(urlparse(iu).path)[1].lower() or ".jpg"
        if ext == ".jpeg":
            ext = ".jpg"
        rel = "sources/%s/images/%s%s" % (KEY, rec["source_id"], ext)
        dest = os.path.join(IMAGES, rec["source_id"] + ext)
        if os.path.exists(dest) and 0 < os.path.getsize(dest) <= MAX_KEEP:
            rec["image_path"] = rel
            continue
        if blocked_note:
            continue
        try:
            st, data = fetch(quote(iu, safe=":/?=&%~+"), binary=True)
        except Blocked as e:
            blocked_note = "Blocked/challenged while fetching images at %s" % e
            continue
        if st == 200 and data and len(data) > 500:
            with open(dest, "wb") as f:
                f.write(data)
            rec["image_path"] = rel
        else:
            log("  image failed", st, iu)

    recipes.sort(key=lambda r: r["source_id"])
    with open(os.path.join(HERE, "recipes.json"), "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, "skipped.json"), "w", encoding="utf-8") as f:
        json.dump(skipped, f, ensure_ascii=False, indent=1)

    # 7. reconciliation report
    canon_set = set(by_canon)
    alias_to_canon = {a: c for c, e in by_canon.items() for a in e["aliases"]}
    sm_recipes = {alias_to_canon[u] for u in sm_urls if u in alias_to_canon}
    land_recipes = {alias_to_canon[u] for u in landing_urls if u in alias_to_canon}
    with_nut = sum(1 for r in recipes if any(v is not None for v in r["nutrients"].values()))
    notes = []
    notes.append("Landing listing says 'Showing %s recipes'; crawled %d cards over all pages (12/page)."
                 % (shown_all, len(landing_urls)))
    notes.append("25 filter listings (special diets, meals & courses, main ingredient) crawled; "
                 "%d recipe URLs appear only in filter listings%s." %
                 (len(filter_only), (": " + ", ".join(filter_only)) if filter_only else ""))
    notes.append("Sitemap: %d URLs under the three recipe paths (/guide-to-diabetes/recipes/, "
                 "/living-with-diabetes/eating/recipes/, /living-with-diabetes/recipes/), "
                 "%d of them recipe pages." % (len(sm_urls), len(sm_recipes)))
    only_sm = sorted(sm_recipes - land_recipes)
    only_land = sorted(land_recipes - sm_recipes)
    notes.append("Recipes in sitemap but not listing: %d%s." % (len(only_sm), (" (" + ", ".join(slug_of(x) for x in only_sm) + ")") if only_sm else ""))
    notes.append("Recipes in listing but not sitemap: %d%s." % (len(only_land), (" (" + ", ".join(slug_of(x) for x in only_land) + ")") if only_land else ""))
    if non_recipes:
        notes.append("Non-recipe pages under recipe paths excluded: %s." % ", ".join(slug_of(x) for x in sorted(non_recipes)))
    dups = {c: e["aliases"] for c, e in by_canon.items() if len(e["aliases"]) > 1}
    if dups:
        notes.append("%d recipes reachable under more than one URL, deduplicated by canonical URL." % len(dups))
    notes.append("Nutrition is per serving ('Each Ng serving contains ...'): kcal, carbs, fibre, protein, "
                 "fat, saturates, sugars, salt, with Low/Medium/High traffic-light labels on fat, saturates, "
                 "sugars and salt; full panel kept in nutrients_raw. sodium_mg = salt g x 400. Sugars are total "
                 "sugars so added_sugar_g is null. Fruit/veg portions go in hints. Diet: Diabetes on all; "
                 "Gluten free -> Gluten-free; Vegan/Vegetarian -> Vegetarian; Dairy free, Nut free, Low fat, "
                 "Low sugar kept in nutrients_raw only. Freezer safe -> dish Freezer. Category from site "
                 "main-ingredient/course filters plus title keywords. image_url is the original upload "
                 "(og:image; some are multi-MB camera files up to 19 MB), while the downloaded copy is the 772px "
                 "'recipe_desktop' rendition shown on the page (originals under 1 MB from the first run kept). "
                 "%d recipes have no photo on the site: %s. robots.txt crawl-delay 5 "
                 "honoured (one request per 5.5s)." % (
                     sum(1 for r in recipes if not r["image_url"]),
                     ", ".join(r["source_id"] for r in recipes if not r["image_url"])))
    if unknown_labels:
        notes.append("Unmapped nutrition labels: %s." % unknown_labels)
    if blocked_note:
        notes.append("INCOMPLETE: " + blocked_note + ". Rerun scrape.py later; it uses the cache.")
    report = {"listed": shown_all if shown_all is not None else len(landing_urls),
              "scraped": len(recipes),
              "with_image": sum(1 for r in recipes if r["image_path"]),
              "with_nutrients": with_nut, "skipped": len(skipped),
              "notes": " ".join(notes)}
    with open(os.path.join(HERE, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    log(json.dumps(report, indent=1))
    log("filter counts:", json.dumps(filter_counts))


if __name__ == "__main__":
    main()
