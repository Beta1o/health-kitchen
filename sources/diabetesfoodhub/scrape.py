#!/usr/bin/env python3
"""Scrape every recipe from the ADA's Diabetes Food Hub (diabetesfoodhub.org).

Discovery: /sitemap.xml (Simple XML Sitemap index -> pages 1..N). robots.txt
disallows "/recipes?" so the listing pager is NOT crawled; the bare /recipes
page is fetched only to read its "N Recipes" total for reconciliation.
English recipe pages live at /recipes/<slug>; the site also publishes Spanish
versions at /es/recipes/<slug> (hreflang pairs in the sitemap). Spanish pages
are kept as lang "es" records (translation_of = English source_id when the
sitemap pairs them). Nothing is translated or filtered here.

Output follows sources/FORMAT.md. Re-runnable: raw pages are cached under
cache/, images are not re-downloaded.  Usage:
    python3 scrape.py            # fetch (cached) + parse + write outputs
    python3 scrape.py fetch      # fetch pages only
    DFH_OFFLINE=1 python3 scrape.py   # cache-only
"""
import collections
import hashlib
import html as htmlmod
import json
import os
import re
import struct
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote, urljoin, unquote

import requests

KEY = "diabetesfoodhub"
SOURCE_NAME = "Diabetes Food Hub (ADA)"
BASE = "https://diabetesfoodhub.org"
SITEMAP = BASE + "/sitemap.xml"
LISTING = BASE + "/recipes"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
IMAGES = os.path.join(HERE, "images")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
WORKERS = 3
MIN_INTERVAL = 1.0           # global spacing between live requests (s)
_pause_until = [0.0]         # global pause after origin 503s
OFFLINE = os.environ.get("DFH_OFFLINE") == "1"
REL_IMG = f"sources/{KEY}/images/"

_lock = threading.Lock()
_last = [0.0]
_challenges = [0]            # consecutive challenge/403 responses
_tls = threading.local()


def session():
    s = getattr(_tls, "s", None)
    if s is None:
        s = requests.Session()
        s.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
        _tls.s = s
    return s


class Blocked(Exception):
    pass


def is_challenge(status, text):
    if status not in (403, 429, 503):
        return False
    t = text or ""
    return ("cf-chl" in t or "Just a moment" in t or "challenge-platform" in t
            or "Attention Required" in t)


def cache_path(url, ext=".html"):
    return os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest() + ext)


def fetch(url, binary=False):
    """Return (status, body). Text pages with status 200/404 are cached."""
    path = cache_path(url, ".bin" if binary else ".html")
    meta = path + ".status"
    if os.path.exists(path):
        st = 200
        if os.path.exists(meta):
            st = int(open(meta).read().strip() or 200)
        if binary:
            return st, open(path, "rb").read()
        return st, open(path, encoding="utf-8").read()
    if OFFLINE:
        return None, None
    if _challenges[0] >= 6:
        raise Blocked(url)
    delay = 3
    for attempt in range(6):
        with _lock:
            wait = max(_last[0] + MIN_INTERVAL, _pause_until[0]) - time.time()
            if wait > 0:
                time.sleep(wait)
            _last[0] = time.time()
        try:
            r = session().get(url, timeout=60)
        except requests.RequestException as e:
            print("  net error", url, e, file=sys.stderr)
            time.sleep(delay)
            delay *= 2
            continue
        if r.status_code == 200 or r.status_code == 404:
            _challenges[0] = 0
            body = r.content if binary else r.text
            if binary:
                if r.status_code == 200:
                    with open(path, "wb") as f:
                        f.write(body)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(body)
                with open(meta, "w") as f:
                    f.write(str(r.status_code))
            return r.status_code, body
        txt = "" if binary else r.text
        if is_challenge(r.status_code, txt) or r.status_code == 403:
            _challenges[0] += 1
            print(f"  challenge/403 ({_challenges[0]}) {url}; backing off {delay * 4}s", file=sys.stderr)
            time.sleep(delay * 4)
            delay *= 2
            if _challenges[0] >= 6:
                raise Blocked(url)
            continue
        if r.status_code == 429 or r.status_code >= 500:
            ra = r.headers.get("Retry-After")
            w = int(ra) if ra and ra.isdigit() else delay * 2
            if attempt >= 3:          # some pages 503 persistently; retried in a later pass
                return r.status_code, None
            with _lock:   # origin "Technical Difficulties" page: pause everybody briefly
                _pause_until[0] = max(_pause_until[0], time.time() + 5)
            print(f"  {r.status_code} {url}; retry in {w}s", file=sys.stderr)
            time.sleep(w)
            delay *= 2
            continue
        return r.status_code, None
    return None, None


# ---------------------------------------------------------------- discovery
def sitemap_entries():
    """Return list of (loc, {hreflang: href}) from every sitemap page."""
    st, idx = fetch(SITEMAP)
    if not idx:
        sys.exit("cannot fetch sitemap")
    pages = re.findall(r"<sitemap>\s*<loc>([^<]+)</loc>", idx) or [SITEMAP]
    out = []
    for p in pages:
        st, x = fetch(htmlmod.unescape(p))
        for b in re.findall(r"<url>(.*?)</url>", x or "", re.S):
            loc = htmlmod.unescape(re.search(r"<loc>(.*?)</loc>", b).group(1).strip())
            alts = {k: htmlmod.unescape(v) for k, v in
                    re.findall(r'hreflang="([\w-]+)"\s+href="([^"]+)"', b)}
            out.append((loc, alts))
    return out


EN_RE = re.compile(r"^https://diabetesfoodhub\.org/recipes/([^/?#]+)$")
ES_RE = re.compile(r"^https://diabetesfoodhub\.org/es/recipes/([^/?#]+)$")


def listing_total():
    st, h = fetch(LISTING)
    m = re.search(r"([\d,]+)\s+Recipes\b", re.sub(r"<[^>]+>", " ", h or ""))
    return int(m.group(1).replace(",", "")) if m else None


def fetch_all(urls):
    def one(u):
        try:
            return u, fetch(u)[0]
        except Blocked:
            return u, "blocked"
    res = {}
    done = 0
    with ThreadPoolExecutor(WORKERS) as ex:
        for u, st in ex.map(one, urls):
            res[u] = st
            done += 1
            if done % 100 == 0:
                print(f"  fetched {done}/{len(urls)}", file=sys.stderr)
    return res


# ---------------------------------------------------------------- parsing
def clean(s):
    if s is None:
        return None
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s).replace("\xa0", " ")
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\s*\n\s*", "\n", s).strip()
    s = re.sub(r"\(\s+", "(", s)
    s = re.sub(r"\s+\)", ")", s)
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    return s.replace("\n", " ").strip() or None


def section(h, start_marker, end_markers):
    i = h.find(start_marker)
    if i < 0:
        return ""
    ends = [h.find(m, i + len(start_marker)) for m in end_markers]
    ends = [e for e in ends if e > 0]
    return h[i:min(ends)] if ends else h[i:]


def jsonld_recipe(h):
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            d = json.loads(m)
        except ValueError:
            continue
        for node in d.get("@graph", [d]) if isinstance(d, dict) else d:
            if isinstance(node, dict) and node.get("@type") == "Recipe":
                return node
    return None


def iso_dur(v):
    """PT1H15M -> '1 hr 15 min'."""
    if not v:
        return None
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:\d+S)?", v.strip())
    if not m or not any(m.groups()):
        return None
    d, hh, mm = (int(x or 0) for x in m.groups())
    hh += d * 24
    parts = []
    if hh:
        parts.append(f"{hh} hr")
    if mm:
        parts.append(f"{mm} min")
    return " ".join(parts) or None


NUM = r"(-?\d+(?:\.\d+)?|\.\d+)"
# label (EN / ES) -> nutrient key; the first match wins, order matters for prefixes
NUT_LABELS = [
    ("calories", r"Calories|Calorías"),
    ("saturated_fat_g", r"Saturated Fat|Grasa Saturada|Grasas Saturadas"),
    ("trans_fat_g", r"Trans Fats?|Grasas? Trans"),
    ("fat_g", r"Total Fat|Grasa Total|Grasas Totales"),
    ("cholesterol_mg", r"Cholesterol|Colesterol"),
    ("sodium_mg", r"Sodium|Sodio"),
    ("carbohydrates_g", r"Total Carbohydrates?|Carbohidratos Totales|Carbohidrato Total"),
    ("fiber_g", r"Dietary Fiber|Fibra dietética|Fibra Dietética"),
    ("added_sugar_g", r"Added Sugars?|Azúcares añadidos|Azúcares Añadidos|Incluye [^<]*azúcares añadidos"),
    ("total_sugar_g", r"Total Sugars?|Azúcares totales|Azúcares Totales|Sugars"),
    ("protein_g", r"Protein|Proteína|Proteínas"),
    ("potassium_mg", r"Potassium|Potasio"),
    ("phosphorus_mg", r"Phosphorus|Fósforo"),
    ("calcium_mg", r"Calcium|Calcio"),
    ("iron_mg", r"Iron|Hierro"),
    ("vitamin_d_mcg", r"Vitamin D|Vitamina D"),
]
FORMAT_NUTS = ["calories", "protein_g", "carbohydrates_g", "fat_g", "cholesterol_mg", "sodium_mg",
               "potassium_mg", "phosphorus_mg", "calcium_mg", "fiber_g", "added_sugar_g"]
_unlabelled = collections.Counter()


def to_num(v):
    v = float(v)
    return int(v) if v == int(v) else v


def parse_nutrition(seg):
    """Return (nutrients dict for FORMAT keys, extra dict, raw text)."""
    body = section(seg, "nutrition__content", ["ingredients-facts-section"]) or seg
    body = re.sub(r"<[^>]*$", "", body[body.find(">") + 1:])
    body = re.sub(r"<h2>.*?</h2>", "", body, flags=re.S)
    body = re.sub(r'<span class="js-servings-label[^>]*>.*?</span>', "", body, flags=re.S)
    # each nutrient is a <li>; take the text directly inside it (nested <ul> handled by splitting)
    pieces = re.split(r"<li[^>]*>|</li>|<ul[^>]*>|</ul>", body)
    vals, raw = {}, []
    for p in pieces:
        t = clean(p)
        if not t:
            continue
        t = re.sub(r"^(Amount per serving|Cantidad por porci[oó]n)\s*", "", t, flags=re.I)
        if re.match(r"^(% Daily value|% Valor diario)", t, re.I):
            continue
        if re.match(r"^(Serving Size|Tamaño de la porción)", t, re.I):
            continue
        raw.append(t)
        m = re.match(r"^(.*?)\s+" + NUM + r"\s*(k?cal|mg|mcg|µg|g)?\b", t)
        if not m:
            continue
        label, val, unit = m.group(1).strip(), m.group(2), (m.group(3) or "").lower()
        for key, pat in NUT_LABELS:
            if re.fullmatch(pat, label, re.I):
                if key in vals:
                    break
                x = to_num(val)
                if key.endswith("_mg") and unit == "g":
                    x = to_num(round(float(val) * 1000, 3))
                elif key.endswith("_g") and unit == "mg":
                    x = to_num(round(float(val) / 1000, 3))
                vals[key] = x
                break
        else:
            _unlabelled[label] += 1
    raw_text = "; ".join(raw) or None
    nutrients = {k: vals.get(k) for k in FORMAT_NUTS}
    extra = {k: v for k, v in vals.items() if k not in FORMAT_NUTS}
    return nutrients, extra, raw_text


def parse_ingredients(h):
    seg = section(h, 'class="ingredients-facts-section"', ['class="shop-ingredients-wrapper"', "ads-block"])
    out, group = [], None
    # tokens: ingredient rows, or anything that looks like a heading between them
    for m in re.finditer(r'<div class="ingredient-wrapper"[^>]*>(.*?)</div>\s*</div>'
                         r'|<(h\d|strong|p)[^>]*>(.*?)</\2>', seg, re.S):
        if m.group(1) is None:
            t = clean(m.group(3))
            if t and t not in ("Ingredients", "Ingredientes"):
                group = t.rstrip(":")
            continue
        row = m.group(1) + "</div>"
        lab = re.search(r'class="ingredient-label">(.*?)</div>', row, re.S)
        us = re.search(r'class="ingredient-us">(.*?)</div>', row, re.S)
        label = clean(lab.group(1)) if lab else None
        qty = clean(us.group(1)) if us else None
        text = " ".join(x for x in (qty, label) if x)
        if text:
            out.append([group, text])
    return out


def parse_steps(h):
    seg = section(h, 'id="recipe-steps-section"', ["</ol>"])
    steps = []
    for li in re.findall(r"<li[^>]*>(.*?)</li>", seg, re.S):
        t = clean(li)
        if t:
            steps.append([None, t])
    if not steps:   # some recipes may use paragraphs instead of a list
        body = re.sub(r"<h3>.*?</h3>", "", seg, flags=re.S)
        for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S):
            t = clean(p)
            if t:
                steps.append([None, t])
    return steps


def parse_page(url, h):
    lang_m = re.search(r'<html[^>]*\blang="([a-z]{2})', h)
    lang = lang_m.group(1) if lang_m else ("es" if "/es/" in url else "en")
    ld = jsonld_recipe(h) or {}
    t = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    title = clean(t.group(1)) if t else clean(ld.get("name"))
    # description: paragraphs between the "How to make" heading and the time/servings block
    desc = None
    dseg = section(h, 'id="recipe-section"', ['class="recipe-preparation-time', 'class="recipe-cook-time',
                                                'class="recipe-servings', 'id="recipe-steps-section"'])
    ps = [clean(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", dseg, re.S)]
    ps = [p for p in ps if p]
    if ps:
        desc = "\n\n".join(ps)
    elif ld.get("description"):
        desc = clean(ld["description"])
    hero = section(h, "recipe-hero__information", ["recipe-hero__img"]) if "recipe-hero__information" in h else ""
    # times / servings from the hero block (first occurrence)
    def span_pair(cls):
        m = re.search(r'class="' + cls + r'[^"]*">.*?<span>(.*?)</span>', h, re.S)
        return clean(m.group(1)) if m else None
    prep = span_pair("recipe-preparation-time") or iso_dur(ld.get("prepTime"))
    cook = span_pair("recipe-cook-time") or iso_dur(ld.get("cookTime"))
    total = iso_dur(ld.get("totalTime"))
    portions = span_pair("recipe-servings") or (clean(str(ld.get("recipeYield"))) if ld.get("recipeYield") else None)
    ss = re.search(r'itemprop="servingSize">(.*?)</div>', h, re.S)
    serving_size = clean(ss.group(1)) if ss else None
    if not serving_size:
        m = re.search(r'class="recipe-serving-size[^"]*">(.*?)</div>', h, re.S)
        serving_size = clean(m.group(1)) if m else None
    tagseg = section(h, 'class="recipe-tags-section"', ["</div>"])
    tags = [(href, clean(txt)) for href, txt in re.findall(r'<a href="([^"]*)"[^>]*>(.*?)</a>', tagseg, re.S)]
    nseg = section(h, 'class="nutrition-facts-section"', ['class="ingredients-facts-section"'])
    nutrients, extra, raw = parse_nutrition(nseg) if nseg else ({k: None for k in FORMAT_NUTS}, {}, None)
    # credits
    credits = []
    for lab, val in re.findall(r"<span\s*>\s*(Recipe by|Source|Photo by|Receta de|Receta por|Fuente|Foto de|Foto por)\s*(.*?)</span>\s*</span>|"
                               r"<span\s*>\s*(?:Recipe by|Source|Photo by)\s*(.*?)</span>", hero, re.S)[:0]:
        pass
    for m in re.finditer(r"<span\s*>\s*([A-Za-zÁÉÍÓÚáéíóúñ ]+?)\s*\n(.*?)</span>\s*(?=<span|</div>)", hero, re.S):
        v = clean(m.group(2))
        if v:
            credits.append(f"{m.group(1).strip()}: {v}")
    img = ld.get("image") or {}
    if isinstance(img, list):
        img = img[0] if img else {}
    img_url = img.get("url") if isinstance(img, dict) else img
    if isinstance(img_url, list):
        img_url = img_url[0] if img_url else None
    if not isinstance(img_url, str) or not img_url.strip():
        img_url = None
    hero_img = section(h, "recipe-hero__img", ["</picture>"])
    hero2x = re.search(r'(/sites/[^"\s]*recipe_hero_banner_720w_2x/[^"\s]+)', hero_img)
    hero1x = re.search(r'<img[^>]+src="([^"]+)"', hero_img)
    return {
        "lang": lang, "title": title, "description": desc, "prep": prep, "cook": cook, "total": total,
        "portions": portions, "serving_size": serving_size, "tags": tags,
        "nutrients": nutrients, "extra": extra, "nutrients_raw": raw,
        "ingredients": parse_ingredients(h), "steps": parse_steps(h), "credits": credits,
        "image_orig": urljoin(BASE, quote(htmlmod.unescape(img_url), safe="/:%?=&")) if img_url else None,
        "image_2x": urljoin(BASE, htmlmod.unescape(hero2x.group(1))) if hero2x else None,
        "image_1x": urljoin(BASE, htmlmod.unescape(hero1x.group(1))) if hero1x else None,
        "has_recipe": bool(ld) or 'id="recipe-steps-section"' in h,
    }


# ---------------------------------------------------------------- mapping
DIET_TAGS = {
    "gluten-free": "Gluten-free", "vegetarian": "Vegetarian", "vegan": "Vegetarian",
    "ckd dialysis": "Dialysis", "ckd non-dialysis": "CKD non-dialysis", "heart healthy": "Heart Healthy",
    "heart-healthy": "Heart Healthy",
}
CUISINES = ["American", "Asian", "Caribbean", "Chinese", "Filipino", "French", "German", "Greek", "Hawaiian",
            "Indian", "Irish", "Italian", "Japanese", "Jewish", "Mediterranean", "Mexican", "Middle Eastern",
            "Native American", "South American", "Southern"]
CUISINE_TAGS = {c.lower(): c for c in CUISINES}
CUISINE_TAGS.update({"mexican/southwestern": "Mexican", "southwestern": "Mexican", "soul food": "Southern",
                     "southern/soul food": "Southern",
                     "middle eastern/north african": "Middle Eastern"})
CUISINE_TITLE = [
    ("Italian", r"\b(lasagna|risotto|pizza|marinara|bolognese|gnocchi|bruschetta|italian|minestrone|caprese|cacciatore|piccata|parmesan chicken|chicken parmesan|eggplant parmesan|frittata|biscotti|pesto)\b"),
    ("Mexican", r"\b(fajitas?|nachos|tacos?|burritos?|quesadillas?|enchiladas?|mexican|tostadas?|pozole|tamales?|huevos rancheros|elote|chilaquiles)\b"),
    ("Indian", r"\b(curry|dal|dhal|tikka|masala|korma|biryani|samosas?|naan|raita|indian|tandoori|chana|paneer)\b"),
    ("Chinese", r"\b(chinese|kung pao|lo mein|chow mein|egg foo young|moo shu|general tso)\b"),
    ("Japanese", r"\b(japanese|teriyaki|sushi|ramen|miso|edamame|soba|udon)\b"),
    ("Greek", r"\b(greek|gyros?|souvlaki|tzatziki|moussaka|spanakopita)\b"),
    ("Caribbean", r"\b(caribbean|jerk|jamaican|cuban|puerto rican)\b"),
    ("French", r"\b(french|ratatouille|quiche|coq au vin|crêpes?|crepes?|niçoise|nicoise|bouillabaisse)\b"),
    ("Middle Eastern", r"\b(shakshuka|falafel|hummus|tagine|shawarma|middle eastern|moroccan|lebanese|za'?atar|tabbouleh|tahini|kofta|baba ganoush)\b"),
    ("Mediterranean", r"\b(mediterranean)\b"),
    ("Asian", r"\b(thai|asian|stir[- ]fry|satay|pad thai|vietnamese|korean|bibimbap|pho|banh mi|sesame|bok choy)\b"),
    ("Hawaiian", r"\b(hawaiian|poke)\b"),
    ("Southern", r"\b(southern|gumbo|jambalaya|cajun|creole|collard greens|grits|hush ?puppies|shrimp and grits)\b"),
]

T = lambda *w: r"\b(" + "|".join(w) + r")\b"
CAT_TITLE = [
    ("Beverages", T("smoothies?", "shakes?", "milkshakes?", "lattes?", "lemonade", "limeade", "cocktails?", "mocktails?",
                    "punch", "spritzers?", "cider", "hot chocolate", "cocoa", "agua fresca", "iced tea", "tea", "coffee",
                    "sangria", "drinks?", "infused water", "water", "batidos?", "licuados?", "bebidas?", "limonada")),
    ("Soups & Stews", T("soups?", "stews?", "chowders?", "bisque", "gumbo", "chili", "chilli", "pozole", "pho", "ramen",
                        "gazpacho", "minestrone", "broth", "sopas?", "caldo", "guisado", "estofado", "crema de")),
    ("Breakfast & Brunch", T("breakfast", "brunch", "pancakes?", "waffles?", "oatmeal", "overnight oats", "oats",
                             "omelets?", "omelettes?", "frittatas?", "granola", "french toast", "scramble", "scrambled eggs",
                             "egg muffins?", "egg cups?", "hash", "huevos", "shakshuka", "quiche", "strata",
                             "desayuno", "avena", "panqueques?", "tortilla de huevo")),
    ("Pizza & Sandwiches", T("pizzas?", "sandwich(es)?", "wraps?", "burgers?", "sliders?", "panini", "pitas?", "flatbreads?",
                             "subs?", "hoagies?", "melts?", "sloppy joes?", "quesadillas?", "tacos?", "burritos?",
                             "lettuce cups", "sándwich(es)?", "hamburguesas?", "envueltos?")),
    ("Salads & Dressings", T("salads?", "slaws?", "coleslaw", "dressing", "vinaigrette", "ensaladas?", "aderezo",
                             "vinagreta")),
    ("Desserts", T("cakes?", "cupcakes?", "cookies?", "brownies?", "blondies?", "pies?", "tarts?", "tartlets?", "pudding",
                   "mousse", "ice cream", "sorbet", "sherbet", "parfaits?", "crisp", "crumble", "cobbler", "cheesecakes?",
                   "bark", "truffles?", "fudge", "popsicles?", "pops", "dessert", "sundae", "custard", "flan", "panna cotta",
                   "macaroons?", "biscotti", "frozen yogurt", "nice cream", "postres?", "pastel", "galletas?", "helado",
                   "budín", "pudín", "flan", "tarta")),
    ("Breads", T("breads?", "muffins?", "biscuits?", "scones?", "rolls?", "loaf", "cornbread", "focaccia", "bagels?",
                 "pan de", "panecillos?")),
    ("Sauces & Seasonings", T("sauce", "salsa", "seasoning", "spice blend", "spice mix", "rub", "marinade", "pesto",
                              "gravy", "chutney", "relish", "glaze", "condiment", "ketchup", "jam", "compote",
                              "aioli", "mayo", "salsas?", "condimento", "aliño", "adobo")),
]
FISH = T("fish", "salmon", "tuna", "cod", "tilapia", "halibut", "trout", "shrimp", "prawns?", "scallops?", "crab",
         "lobster", "mussels", "clams", "oysters", "seafood", "catfish", "mahi[- ]mahi", "sardines?", "anchov(y|ies)",
         "snapper", "flounder", "sole", "haddock", "pollock", "swordfish", "bass", "calamari", "squid", "pescado",
         "salmón", "atún", "camarones?", "gambas", "mariscos", "bacalao", "tilapia")
POULTRY = T("chicken", "turkey", "hen", "duck", "pollo", "pavo")
MEAT = T("beef", "steak", "pork", "lamb", "ham", "bacon", "sausages?", "meatballs?", "meatloaf", "veal", "brisket",
         "sirloin", "tenderloin", "ribs?", "chops?", "prosciutto", "pepperoni", "carne", "res", "cerdo", "cordero",
         "jamón", "tocino", "salchichas?", "albóndigas?", "bistec", "lomo", "meat ?loaf", "eye of round",
         "pot roast", "roast beef", "kielbasa", "chorizo")
GRAINS = T("pasta", "spaghetti", "noodles?", "macaroni", "mac", "penne", "linguine", "fettuccine", "lasagna", "orzo",
           "ravioli", "tortellini", "gnocchi", "rigatoni", "ziti", "rotini", "fusilli", "farfalle", "tortellini", "rice", "risotto", "quinoa", "couscous", "farro", "barley", "bulgur",
           "polenta", "grits", "grain bowl", "grains?", "pilaf", "paella", "arroz", "fideos", "espaguetis?")
DESSERTISH = T("cookies?", "cakes?", "brownies?", "pies?", "tarts?", "crisp", "cobbler", "pudding", "ice cream")
SAVOURY_WORDS = T("savory", "savoury", "shepherd[’']?s", "lasagna", "vegetables?", "veggies?", "artichokes?", "quinoa",
                  "cauliflower", "provencal", "provençal", "spinach", "root vegetable", "tilapia", "potato", "zucchini cakes",
                  "corn cakes", "salmon", "crab", "tuna", "black bean", "lentil")
SAVOURY = T("pot pie", "chicken pie", "shepherd'?s pie", "tamale pie", "pizza", "quiche", "crab cakes?", "fish cakes?",
            "salmon cakes?", "tuna cakes?", "rice cakes?", "potato cakes?", "corn cakes?", "veggie cakes?")


def tagnames(tags):
    return [htmlmod.unescape(t or "").strip().lower() for _, t in tags]


def pick_category(title, tags, ing_text):
    t = (title or "").lower()
    tg = set(tagnames(tags))
    savoury = re.search(SAVOURY, t)
    if "beverages" in tg or "drinks" in tg:
        return "Beverages"
    protein = re.search(FISH + "|" + POULTRY + "|" + MEAT, t)
    head = re.split(r"\b(with|w/|over|and|con|y)\b", t)[0]   # the dish itself, before "with ... sauce"
    for cat, pat in CAT_TITLE:
        if not re.search(pat, t):
            continue
        if cat == "Beverages" and (protein or re.search(r"\b(braised|cabbage|tea[- ]smoked|tea[- ]rubbed)\b|water ?chestnut|watercress|watermelon (salad|salsa)", t)):
            continue
        if cat == "Desserts" and (savoury or protein or re.search(SAVOURY_WORDS, t)):
            continue
        if cat == "Breads" and (protein or re.search(r"\b(meat ?loaf|egg rolls?|spring rolls?|summer rolls?|cabbage rolls?|lasagna rolls?|roll[- ]ups?|sushi rolls?)\b", t)):
            continue
        if cat == "Sauces & Seasonings" and (protein or re.search(GRAINS, t) or not re.search(pat, head)):
            continue
        return cat
    if "dessert" in tg or "desserts" in tg:
        return "Desserts"
    if "breakfast and brunch" in tg or "breakfast" in tg:
        return "Breakfast & Brunch"
    if re.search(FISH, t):
        return "Fish & Seafood"
    if re.search(POULTRY, t):
        return "Chicken & Turkey"
    if re.search(MEAT, t):
        return "Beef, Lamb & Pork"
    if re.search(GRAINS, t):
        return "Pasta, Rice & Grains"
    if tg & {"soup", "soups", "soups & stews"}:
        return "Soups & Stews"
    if tg & {"salads"}:
        return "Salads & Dressings"
    if tg & {"sandwiches"}:
        return "Pizza & Sandwiches"
    if tg & {"sauces", "salad dressings & condiments"}:
        return "Sauces & Seasonings"
    if tg & {"appetizers", "snacks"}:
        return "Appetizers & Snacks"
    if "seafood" in tg:
        return "Fish & Seafood"
    if tg & {"main dish"}:
        ing = (ing_text or "").lower()
        for cat, pat in (("Fish & Seafood", FISH), ("Chicken & Turkey", POULTRY), ("Beef, Lamb & Pork", MEAT)):
            if re.search(pat, ing):
                return cat
    return "Vegetables"


def pick_diet(tags):
    out = ["Diabetes"]
    for n in tagnames(tags):
        d = DIET_TAGS.get(n)
        if d and d not in out:
            out.append(d)
    return out


def pick_cuisine(title, tags):
    out = []
    for n in tagnames(tags):
        c = CUISINE_TAGS.get(n)
        if c and c not in out:
            out.append(c)
    t = (title or "").lower()
    for c, pat in CUISINE_TITLE:
        if c not in out and re.search(pat, t):
            out.append(c)
    return out


def pick_method(title, tags, steps_text):
    tg = set(tagnames(tags))
    t = ((title or "") + " " + (steps_text or "")).lower()
    out = []
    if "slow cooker" in tg or re.search(r"slow[- ]cooker|crock[- ]?pot", t):
        out.append("Slow Cooker")
    if "no cook" in tg:
        out.append("No Cooking")
    if "grilling" in tg:
        out.append("Grill")
    if re.search(r"\bmicrowav", t):
        out.append("Microwave")
    if re.search(r"\b(bake|baked|baking)\b", t):
        out.append("Bake")
    if re.search(r"\b(oven|broil|broiler)\b", t):
        out.append("Oven")
    if re.search(r"\b(roast|roasted|roasting)\b", t):
        out.append("Roast")
    if re.search(r"\b(grill|grilled|grilling|grill pan)\b", t) and "Grill" not in out:
        out.append("Grill")
    if re.search(r"\b(deep[- ]fry|pan[- ]fry|fry|frying|air[- ]fry(er)?)\b", t):
        out.append("Fry")
    if re.search(r"\b(skillet|saucepan|stockpot|stovetop|stove|wok|dutch oven|pot over|(low|medium|high|medium[- ]high|medium[- ]low) heat|simmer|boil|saut[eé])", t):
        out.append("Stove Top")
    return out


def pick_dish(title, tags, n_ing, category, diet):
    tg = set(tagnames(tags))
    t = (title or "").lower()
    out = []
    add = lambda x: x not in out and out.append(x)
    if "quick & easy" in tg:
        add("Quick"); add("Easy")
    if "budget friendly" in tg:
        add("Budget")
    if n_ing and n_ing <= 5:
        add("5 or less ingredients")
    if re.search(r"\b(soups?|chowder|bisque|gazpacho)\b", t):
        add("Soup")
    if re.search(r"\b(stews?|chili|gumbo|ragout)\b", t):
        add("Stew")
    if re.search(r"\bstir[- ]?fr(y|ied)\b", t):
        add("Stir-fry")
    if re.search(r"\bmuffins?\b", t):
        add("Muffin")
    if re.search(r"\b(cakes?|cupcakes?|cheesecakes?)\b", t) and category == "Desserts":
        add("Cake")
    if re.search(r"\bcookies?\b", t):
        add("Cookies")
    if re.search(r"\b(pies?|tarts?)\b", t) and not re.search(SAVOURY, t):
        add("Pie")
    if category == "Breads":
        add("Bread")
    if "one pot" in tg:
        add("One-Dish Meal")
    if re.search(r"\b(one[- ]pot|one[- ]pan|sheet[- ]pan|casserole|skillet dinner|one[- ]skillet)\b", t):
        add("One-Dish Meal")
    if "main dish" in tg and "Vegetarian" in diet:
        add("Meatless Entree")
    return out


# ---------------------------------------------------------------- images
def image_size(b):
    """(width, height) from JPEG/PNG/WebP bytes, or None."""
    try:
        if b[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", b[16:24])
        if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
            if b[12:16] == b"VP8X":
                return (int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1)
            if b[12:16] == b"VP8 ":
                w, h = struct.unpack("<HH", b[26:30])
                return (w & 0x3FFF, h & 0x3FFF)
            if b[12:16] == b"VP8L":
                v = int.from_bytes(b[21:25], "little")
                return ((v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1)
        if b[:2] == b"\xff\xd8":
            i = 2
            while i < len(b) - 9:
                if b[i] != 0xFF:
                    i += 1
                    continue
                mk = b[i + 1]
                if mk in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    hh, ww = struct.unpack(">HH", b[i + 5:i + 9])
                    return (ww, hh)
                if mk in (0xD8, 0x01) or 0xD0 <= mk <= 0xD7:
                    i += 2
                    continue
                i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    except (struct.error, IndexError):
        pass
    return None


def ext_of(b):
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        return ".webp"
    if b[:2] == b"\xff\xd8":
        return ".jpg"
    if b[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    return None


def download_image(sid, cands):
    """Try candidate URLs (original first); keep the first that is an image <= 1600 px wide.
    Returns (image_url, image_path) where image_url is the original full-size URL."""
    for f in os.listdir(IMAGES) if os.path.isdir(IMAGES) else []:
        if os.path.splitext(f)[0] == sid:
            return os.path.join(REL_IMG, f)
    for u in [c for c in cands if c]:
        try:
            st, b = fetch(u, binary=True)
        except Blocked:
            return None
        if st != 200 or not b:
            continue
        ext = ext_of(b)
        if not ext:
            continue
        sz = image_size(b)
        if sz and sz[0] > 1600 and u != cands[-1]:
            continue          # too wide: fall back to the 1440 px hero rendition
        with open(os.path.join(IMAGES, sid + ext), "wb") as f:
            f.write(b)
        return os.path.join(REL_IMG, sid + ext)
    return None


# ---------------------------------------------------------------- build
def record(url, sid, p, lang, translation_of=None):
    ing_text = " ".join(x for _, x in p["ingredients"])
    steps_text = " ".join(x for _, x in p["steps"])
    cat = pick_category(p["title"], p["tags"], ing_text)
    diet = pick_diet(p["tags"])
    return {
        "source": KEY, "source_name": SOURCE_NAME, "source_id": sid, "url": url, "lang": lang,
        "title": p["title"], "description": p["description"],
        "image_url": p["image_orig"] or p["image_2x"] or p["image_1x"], "image_path": None,
        "portions": p["portions"], "serving_size": p["serving_size"],
        "category": cat, "diet": diet,
        "dish": pick_dish(p["title"], p["tags"], len(p["ingredients"]), cat, diet),
        "cuisine": pick_cuisine(p["title"], p["tags"]),
        "method": pick_method(p["title"], p["tags"], steps_text),
        "nutrients": p["nutrients"], "nutrients_raw": p["nutrients_raw"],
        "ingredients": p["ingredients"], "steps": p["steps"], "hints": [],
        "food_choices": [], "carb_choices": None, "video_url": None,
        "prep_time": p["prep"], "cook_time": p["cook"], "total_time": p["total"],
        "translation_of": translation_of,
        "tags": [t for _, t in p["tags"]],
        "credits": p["credits"],
        "nutrients_extra": p["extra"],
    }


def build(en, es, total, status):
    skipped, parsed = [], {}
    for loc, _ in en + es:
        st = status.get(loc)
        if st == "blocked":
            skipped.append({"url": loc, "reason": "blocked (Cloudflare/403); not retried"})
            continue
        st, h = fetch(loc) if st != "blocked" else (None, None)
        if st != 200 or not h:
            skipped.append({"url": loc, "reason": f"HTTP {st}" if st else "fetch failed (repeated 503 'Technical Difficulties')"})
            continue
        p = parse_page(loc, h)
        if not p["has_recipe"] or not (p["ingredients"] or p["steps"]):
            skipped.append({"url": loc, "reason": "page has no recipe content"})
            continue
        parsed[loc] = p

    # learn ES->EN tag names from paired pages (tags are listed in the same order)
    es_tag = collections.Counter()
    for loc, alts in es:
        en_url = alts.get("en")
        if loc in parsed and en_url in parsed:
            a, b = parsed[en_url]["tags"], parsed[loc]["tags"]
            if len(a) == len(b):
                for (_, x), (_, y) in zip(a, b):
                    es_tag[(y, x)] += 1
    es_map = {}
    for (y, x), n in es_tag.most_common():
        es_map.setdefault(y, x)

    recipes, en_ids = [], {}
    for loc, alts in en:
        if loc not in parsed:
            continue
        p = parsed[loc]
        sid = EN_RE.match(loc).group(1)
        r = record(loc, sid, p, p["lang"])
        recipes.append(r)
        en_ids[loc] = r
    for loc, alts in es:
        if loc not in parsed:
            continue
        p = parsed[loc]
        sid = "es-" + ES_RE.match(loc).group(1)
        en_url = alts.get("en")
        base = en_ids.get(en_url)
        if not base:
            p = dict(p, tags=[(h_, es_map.get(t, t)) for h_, t in p["tags"]])
        r = record(loc, sid, p, p["lang"], base["source_id"] if base else None)
        r["tags"] = [t for _, t in parsed[loc]["tags"]]
        if base:   # same recipe: share the English classification
            for k in ("category", "diet", "dish", "cuisine", "method"):
                r[k] = base[k]
        recipes.append(r)

    # images: download once per distinct photo
    by_photo = {}
    def get_img(r):
        p = parsed[r["url"]]
        key = r["image_url"]
        if not key:
            return
        if key in by_photo:
            r["image_path"] = by_photo[key]
            return
        cands = [p["image_orig"], p["image_2x"], p["image_1x"]]
        cands = list(dict.fromkeys(c for c in cands if c))
        path = download_image(r["source_id"], cands)
        by_photo[key] = path
        r["image_path"] = path
    en_first = [r for r in recipes if not r["translation_of"]] + [r for r in recipes if r["translation_of"]]
    for i, r in enumerate(en_first, 1):
        get_img(r)
        if i % 200 == 0:
            print(f"  images {i}/{len(en_first)}", file=sys.stderr)

    with open(os.path.join(HERE, "recipes.json"), "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, "skipped.json"), "w", encoding="utf-8") as f:
        json.dump(skipped, f, ensure_ascii=False, indent=1)

    def stats(rs):
        return {"scraped": len(rs), "with_image": sum(1 for r in rs if r["image_path"]),
                "with_nutrients": sum(1 for r in rs if any(v is not None for v in r["nutrients"].values()))}
    s_all = stats(recipes)
    s_en = stats([r for r in recipes if r["lang"] == "en"])
    s_es = stats([r for r in recipes if r["lang"] == "es"])
    paired = sum(1 for r in recipes if r["translation_of"])
    listed = len(en) + len(es)
    notes = (
        f"Discovery via sitemap.xml only (robots.txt disallows '/recipes?', so the listing pager was not crawled). "
        f"The /recipes listing header says {total} recipes; the sitemap has {len(en)} English /recipes/<slug> URLs "
        f"and {len(es)} Spanish /es/recipes/<slug> URLs (listed = {len(en)} + {len(es)} = {listed}). "
        f"Spanish pages are the site's own translations, kept as lang 'es' records with source_id 'es-<slug>'; "
        f"{paired} are linked by hreflang to their English page (translation_of = English source_id, sharing its "
        f"category/diet/dish/cuisine/method and photo), the rest have no English alternate in the sitemap and stand "
        f"alone. lang comes from <html lang>. Per language: en {s_en}, es {s_es}. "
        f"Parsed from page HTML (the JSON-LD splits ingredients/steps on commas and omits potassium). Nutrition panel "
        f"mapped per serving; added_sugar_g only from the 'Added Sugars' row; saturated/trans fat and total sugars "
        f"are kept in nutrients_extra. No phosphorus/calcium values or diabetes exchanges/choices appear on the "
        f"pages, so food_choices/carb_choices are empty. Ingredient text = US quantity + name (+ note); the metric "
        f"column is ignored. diet: 'Diabetes' for all, plus tags Gluten-Free, Vegetarian/Vegan, CKD Dialysis -> "
        f"Dialysis, CKD Non-Dialysis -> CKD non-dialysis ('Kidney-Friendly', 'Low Sodium', 'Low Carb' have no "
        f"matching value). Extra fields kept per record: tags, credits, nutrients_extra. Origin intermittently "
        f"returned HTTP 503 'Technical Difficulties' pages (not a bot challenge); these were retried with backoff."
    )
    report = {"listed": listed, "scraped": s_all["scraped"], "with_image": s_all["with_image"],
              "with_nutrients": s_all["with_nutrients"], "skipped": len(skipped), "notes": notes}
    with open(os.path.join(HERE, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(json.dumps(report, indent=1, ensure_ascii=False))
    if _unlabelled:
        print("unmapped nutrition labels:", dict(_unlabelled), file=sys.stderr)



def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(IMAGES, exist_ok=True)
    entries = sitemap_entries()
    en = [(l, a) for l, a in entries if EN_RE.match(l)]
    es = [(l, a) for l, a in entries if ES_RE.match(l)]
    total = listing_total()
    print(f"sitemap: {len(en)} /recipes/ + {len(es)} /es/recipes/; listing says {total}")
    status = fetch_all([l for l, _ in en] + [l for l, _ in es])
    for rnd in range(2):   # second/third chance for pages that kept returning 503
        failed = [u for u, st in status.items() if st not in (200, 404, "blocked")]
        if not failed or OFFLINE:
            break
        print(f"retrying {len(failed)} failed pages in 60s", file=sys.stderr)
        time.sleep(60)
        status.update(fetch_all(failed))
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        print({k: sum(1 for v in status.values() if v == k) for k in set(status.values())})
        return
    build(en, es, total, status)


if __name__ == "__main__":
    main()
