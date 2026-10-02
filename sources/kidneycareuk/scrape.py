#!/usr/bin/env python3
"""Scrape every Kidney Kitchen recipe from Kidney Care UK.

Discovery: recipe index (all pages), every quick-filter listing (all pages),
themed collection pages, and the sitemap. Output follows sources/FORMAT.md.
Re-runnable: raw pages are cached under cache/, images are not re-downloaded.
"""
import hashlib
import html
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

import requests

KEY = "kidneycareuk"
SOURCE_NAME = "Kidney Care UK"
BASE = "https://kidneycareuk.org"
KK = BASE + "/get-support/healthy-diet-support/kidney-kitchen/"
INDEX = KK + "recipe-index/"
SITEMAP = BASE + "/sitemap.xml"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
IMAGES = os.path.join(HERE, "images")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
WORKERS = 1
OFFLINE = os.environ.get("KCUK_OFFLINE") == "1"   # cache-only run
MIN_INTERVAL = 3.0   # seconds between live requests (Cloudflare rate-limits bursts with 403/1106)
_last = [0.0]
_lock = __import__("threading").Lock()
_blocked = [0]       # consecutive 403s; stop hitting the site after a few

session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"})

RECIPE_RE = re.compile(r"https://kidneycareuk\.org/get-support/healthy-diet-support/"
                       r"kidney-kitchen/recipe-index/([a-z0-9][a-z0-9-]*)/")
NON_RECIPE_SLUGS = {"quick-filter", "search", "page"}


# ---------------------------------------------------------------- fetching
def fetch(url, binary=False, use_cache=True):
    """Return (status, body). Caches successful text pages."""
    path = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest() + ".html")
    if use_cache and not binary and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return 200, f.read()
    if _blocked[0] >= 5 or (OFFLINE and not binary):
        return 403, None
    delay = 2
    for attempt in range(6):
        with _lock:
            wait = _last[0] + MIN_INTERVAL - time.time()
            if wait > 0:
                time.sleep(wait)
            _last[0] = time.time()
        try:
            r = session.get(url, timeout=40)
        except requests.RequestException as e:
            print("  err", url, e, file=sys.stderr)
            time.sleep(delay)
            delay *= 2
            continue
        if r.status_code == 429 or r.status_code >= 500:
            ra = r.headers.get("Retry-After")
            time.sleep(int(ra) if ra and ra.isdigit() else delay)
            delay *= 2
            continue
        if r.status_code == 403:
            _blocked[0] += 1
            return 403, None
        if r.status_code != 200:
            return r.status_code, None
        _blocked[0] = 0
        if binary:
            return 200, r.content
        text = r.text
        # Treat a redirect away from the requested page as a final URL note.
        if r.url.rstrip("/") != url.split("#")[0].split("?")[0].rstrip("/") and "?" not in url:
            text = "<!-- final-url: %s -->\n" % r.url + text
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return 200, text
    return -1, None


# ---------------------------------------------------------------- helpers
def clean(s):
    if s is None:
        return None
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


def paras(fragment):
    """Split a rich-text fragment into paragraph/list-item texts."""
    parts = re.findall(r"<(p|li|h[2-6])[^>]*>(.*?)</\1>", fragment, re.S)
    out = [clean(t) for _, t in parts]
    out = [t for t in out if t]
    if not out:
        t = clean(fragment)
        if t:
            out = [t]
    return out


def between(s, start_pat, end_pat):
    m = re.search(start_pat, s, re.S)
    if not m:
        return None
    e = re.search(end_pat, s[m.end():], re.S)
    return s[m.end(): m.end() + e.start()] if e else s[m.end():]


def recipe_links(page):
    out = []
    for m in RECIPE_RE.finditer(page):
        slug = m.group(1)
        if slug not in NON_RECIPE_SLUGS:
            out.append(slug)
    return out


def listing_links(page):
    """Recipe slugs from listing cards only (not the related/featured blocks)."""
    out = []
    for m in re.finditer(r'card-group__card--recipe(.*?)</li>', page, re.S):
        out += recipe_links(m.group(1))
    return out


def crawl_listing(base_url):
    """Follow pagination of a listing; return (ordered slugs, pages crawled)."""
    slugs, page_no, seen_pages = [], 1, 0
    while True:
        url = base_url if page_no == 1 else base_url + ("&" if "?" in base_url else "?") + "page=%d" % page_no
        st, body = fetch(url)
        if body is None:
            break
        seen_pages += 1
        got = listing_links(body)
        new = [s for s in got if s not in slugs]
        slugs += new
        if not new or 'pagination__next' not in body:
            break
        page_no += 1
        if page_no > 60:
            break
    return slugs, seen_pages


# ---------------------------------------------------------------- mapping
CATS = [
    ("Beverages", r"\b(smoothie|milkshake|shake|lemonade|drink|punch|cordial|mocktail|latte|hot chocolate|spritzer|iced tea)\b"),
    ("Soups & Stews", r"\b(soup|stew|broth|chowder|casserole|hotpot|goulash|tagine|dal|daal|dhal|chilli con carne|bisque|minestrone|gumbo|potjie)\b"),
    ("Salads & Dressings", r"\b(salad|slaw|coleslaw|dressing|vinaigrette)\b"),
    ("Sauces & Seasonings", r"\b(sauce|gravy|pesto|salsa|seasoning|spice mix|spice blend|marinade|chutney|relish|dip|hummus|houmous|raita|stock|mayonnaise|jam|curd)\b"),
    ("Desserts", r"\b(cake|cupcakes?|brownies?|cookies?|biscuits?|tart|crumble|pudding|mousse|cheesecake|trifle|ice cream|sorbet|meringues?|pavlova|fudge|truffles?|flapjacks?|shortbread|blondies?|dessert|ricciarelli|macaroons?|panna cotta|custard|fool|eton mess|mince pies?|sweets?|lollies|lolly|tiffin|rocky road|doughnuts?|churros|pie with|crème|creme|sundae|parfait|bites|bark|biscotti|cobbler|strudel|roulade|torte|gateau|millionaire|traybake|bakewell|treacle|sponge|muffins? with cream|frosting|baklava|kheer|halwa|gulab|ladoo|barfi|jelly)\b"),
    ("Breakfast & Brunch", r"\b(breakfast|porridge|overnight oats|granola|muesli|pancakes?|waffles?|french toast|omelette|frittata|scrambled|shakshuka|eggs benedict|crumpets?|brunch|bircher|hash browns?)\b"),
    ("Breads", r"\b(bread|loaf|rolls?|scones?|muffins?|soda bread|focaccia|naan|chapati|chapatti|roti|paratha|flatbreads?|bagels?|buns?|teacakes?|pitta bread|dumplings|cornbread|bannock|puri)\b"),
    ("Pizza & Sandwiches", r"\b(pizza|sandwich(es)?|toastie|wraps?|burgers?|pittas?|quesadillas?|tacos?|burritos?|calzone|panini|sliders?|baps?|hot dogs?|bruschetta|subs?|fajitas|nachos|kebabs?|gyros?|enchiladas)\b"),
    ("Fish & Seafood", r"\b(fish|salmon|tuna|cod|haddock|prawns?|shrimp|mackerel|sardines?|trout|seafood|crab|mussels?|scampi|plaice|pollock|hake|tilapia|sea bass|squid|kedgeree)\b"),
    ("Chicken & Turkey", r"\b(chicken|turkey|duck)\b"),
    ("Beef, Lamb & Pork", r"\b(beef|lamb|pork|sausages?|bacon|ham|mince|steak|meatballs?|gammon|chorizo|bolognese|cottage pie|shepherd'?s pie|keema|burger)\b"),
    ("Pasta, Rice & Grains", r"\b(pasta|spaghetti|penne|lasagne|lasagna|macaroni|macaro|mac|noodles?|rice|risotto|couscous|orzo|tagliatelle|fusilli|linguine|gnocchi|paella|pilau|pilaf|biryani|jollof|quinoa|bulgur|polenta|ravioli|carbonara|arrabbiata|puttanesca|farfalle|rigatoni|fettuccine|congee|barley|grains?)\b"),
    ("Appetizers & Snacks", r"\b(snacks?|bites|crisps|popcorn|samosas?|pakoras?|bhajis?|fritters?|spring rolls?|canap[eé]s|nibbles|crackers?|skewers|wings|nuggets|goujons|dippers|starter|appetiser|appetizer|sausage rolls?|vol[- ]au[- ]vents?|tapas|pinwheels?|croquettes?|arancini|tikki|bhaji|chaat|scotch eggs?)\b"),
    ("Vegetables", r"\b(vegetables?|veg|potato(es)?|cauliflower|broccoli|cabbage|carrots?|courgettes?|aubergines?|peppers?|mushrooms?|spinach|beans?|lentils?|chickpeas?|tofu|squash|pumpkin|leeks?|onions?|parsnips?|swede|sweetcorn|corn|peas|greens|chips|wedges|ratatouille|curry|stir[- ]fry|tempeh|halloumi|quiche|tart|bake|roast)\b"),
]


SAVOURY = r"\b(chicken|turkey|beef|lamb|pork|sausages?|fish|salmon|tuna|cod|prawns?|pasta|rice|curry|chilli|potato(es)?|beans?|lentils?|cheese and|vegetable|tofu|mince|eggs?|quiche|pie and)\b"
ORDER = ["Beverages", "Soups & Stews", "Fish & Seafood", "Chicken & Turkey", "Beef, Lamb & Pork",
         "Salads & Dressings", "Pizza & Sandwiches", "Pasta, Rice & Grains", "Breakfast & Brunch",
         "Desserts", "Breads", "Sauces & Seasonings", "Appetizers & Snacks", "Vegetables"]
CATPAT = dict(CATS)


def pick_category(title, course, ingredients_text):
    t = title.lower()
    course = [c.lower() for c in course]
    savoury = re.search(SAVOURY, t)
    if "dessert" in course and not savoury and not re.search(r"\b(soup|salad)\b", t):
        return "Desserts"
    for cat in ORDER:
        if re.search(CATPAT[cat], t):
            if cat == "Desserts" and savoury:
                continue
            if cat == "Breads" and re.search(r"\b(sausage rolls?|spring rolls?)\b", t):
                return "Appetizers & Snacks"
            return cat
    if "breakfast" in course:
        return "Breakfast & Brunch"
    if "snack" in course:
        return "Appetizers & Snacks"
    ing = (ingredients_text or "").lower()
    for cat in ("Fish & Seafood", "Chicken & Turkey", "Beef, Lamb & Pork"):
        if re.search(CATPAT[cat], ing):
            return cat
    return "Vegetables"


CUISINE_TITLE = [
    ("Italian", r"\b(lasagne|pasta|risotto|pizza|arrabbiata|puttanesca|carbonara|bolognese|gnocchi|focaccia|bruschetta|italian|ricciarelli|tiramisu|minestrone|panna cotta|calzone|frittata|biscotti)\b"),
    ("Mexican", r"\b(fajitas?|nachos|tacos?|burritos?|quesadillas?|enchiladas?|mexican|salsa|chilli con carne|churros)\b"),
    ("Indian", r"\b(curry|dal|daal|dhal|tikka|masala|korma|biryani|pilau|samosas?|pakoras?|bhajis?|chapati|chapatti|naan|roti|paratha|raita|indian|keema|tandoori|kheer|chaat|aloo|saag|paneer)\b"),
    ("Chinese", r"\b(chinese|sweet and sour|chow mein|kung pao|egg fried rice|spring rolls?|char siu)\b"),
    ("Japanese", r"\b(japanese|teriyaki|katsu|sushi|ramen|miso)\b"),
    ("Greek", r"\b(greek|gyros?|souvlaki|tzatziki|moussaka|spanakopita)\b"),
    ("Caribbean", r"\b(caribbean|jerk|jamaican|plantain|rice and peas)\b"),
    ("French", r"\b(french|ratatouille|quiche|crème brûlée|creme brulee|coq au vin|crêpes?|crepes?|bourguignon)\b"),
    ("Middle Eastern", r"\b(shakshuka|falafel|hummus|houmous|tagine|shawarma|middle eastern|moroccan|lebanese|za'?atar|tabbouleh)\b"),
    ("Mediterranean", r"\b(mediterranean)\b"),
    ("Asian", r"\b(thai|asian|stir[- ]fry|satay|laksa|pad thai|vietnamese|korean|malaysian|noodles)\b"),
    ("Irish", r"\b(irish|colcannon|soda bread)\b"),
]


def pick_cuisine(title):
    t = title.lower()
    return [c for c, p in CUISINE_TITLE if re.search(p, t)]


def pick_method(title, steps_text):
    t = (title + " " + steps_text).lower()
    out = []
    if "slow cooker" in t:
        out.append("Slow Cooker")
    if "microwave" in t:
        out.append("Microwave")
    if re.search(r"\b(bake|baked|baking)\b", t):
        out.append("Bake")
    if re.search(r"\b(oven|preheat the oven|gas mark)\b", t):
        out.append("Oven")
    if re.search(r"\b(roast|roasted|roasting)\b", t):
        out.append("Roast")
    if re.search(r"\b(grill|grilled|griddle|bbq|barbecue)\b", t):
        out.append("Grill")
    if re.search(r"\b(fry|fried|frying|air fryer|air-fryer)\b", t):
        out.append("Fry")
    if re.search(r"\b(hob|saucepan|frying pan|simmer|wok)\b", t):
        out.append("Stove Top")
    return out


NUM_RE = re.compile(r"(<\s*)?(\d+(?:\.\d+)?)\s*(kcals?|kcal|calories|kj|mg|g|mmol)?\b", re.I)


def parse_nutrients(items, portions):
    """items: list of (label, value) numeric-ish entries. Returns dict + notes."""
    n = {k: None for k in ("calories", "protein_g", "carbohydrates_g", "fat_g",
                           "cholesterol_mg", "sodium_mg", "potassium_mg",
                           "phosphorus_mg", "calcium_mg", "fiber_g", "added_sugar_g")}
    unknown = []
    for label, val in items:
        l = label.lower().rstrip(":").strip()
        m = NUM_RE.search(val.replace(",", ""))
        if not m:
            continue
        x = float(m.group(2))
        unit = (m.group(3) or "").lower()

        def put(key, v):
            if n[key] is None:
                n[key] = round(v, 1) if v % 1 else int(v)

        if l in ("energy", "calories", "kcal", "energy (kcal)"):
            if unit == "kj":
                continue
            put("calories", x)
        elif l.startswith("carbohydrate"):
            put("carbohydrates_g", x)
        elif l.startswith("protein"):
            put("protein_g", x)
        elif l in ("fat", "total fat"):
            put("fat_g", x)
        elif l.startswith("fibre") or l.startswith("fiber"):
            put("fiber_g", x)
        elif l.startswith("sodium"):
            put("sodium_mg", x * 23 if unit == "mmol" else (x * 1000 if unit == "g" else x))
        elif l.startswith("potassium"):
            put("potassium_mg", x * 39.1 if unit == "mmol" else (x * 1000 if unit == "g" else x))
        elif l.startswith("phosph"):
            put("phosphorus_mg", x * 31 if unit == "mmol" else (x * 1000 if unit == "g" else x))
        elif l.startswith("calcium"):
            put("calcium_mg", x * 1000 if unit == "g" else x)
        elif l.startswith("cholesterol"):
            put("cholesterol_mg", x)
        elif l in ("added sugar", "added sugars"):
            put("added_sugar_g", x)
        else:
            unknown.append(label)
    return n, unknown


# ---------------------------------------------------------------- recipe parse
def parse_recipe(slug, page):
    url = INDEX + slug + "/"
    m = re.search(r"<!-- final-url: (\S+) -->", page)
    if m:
        url = m.group(1)
    title = clean(between(page, r'<h1 class="recipe__title"[^>]*>', r"</h1>"))
    body = between(page, r'<main', r'<section class="base-section"') or page
    if not title or ('recipe__ingredients' not in body and 'recipe__card-steps' not in body):
        return None

    card = between(body, r'class="recipe__card-body"', r'<aside') or ""
    image_url = None
    fig = re.search(r"<figure>(.*?)</figure>", card, re.S)
    if fig:
        srcset = re.search(r'srcset="([^"]+)"', fig.group(1))
        best, bw = None, -1
        if srcset:
            for part in srcset.group(1).split(","):
                bits = part.strip().split()
                if len(bits) == 2 and bits[1].endswith("w"):
                    w = int(bits[1][:-1])
                    if w > bw:
                        best, bw = bits[0], w
        if not best:
            src = re.search(r'src="([^"]+)"', fig.group(1))
            best = src.group(1) if src else None
        image_url = best

    tags = [clean(t) for t in re.findall(r'<li class="recipe__card-tag">(.*?)</li>', card, re.S)]
    tags = [t for t in tags if t]
    intro = between(card, r'class="recipe__card-introduction"', r"</div>\s*</div>")
    description = " ".join(paras(intro)) if intro else None
    pdf = re.search(r'href="([^"]+\.pdf)"[^>]*class="recipe__card-download"', card)

    aside = between(body, r'<aside class="recipe__card-sidebar"', r"</aside>") or ""
    meta = {}
    for lab, val in re.findall(r'recipe__card-sidebar-list-label">(.*?)</span>(.*?)</li>', aside, re.S):
        meta[clean(lab).rstrip(":").lower()] = clean(val)
    nut_section = between(aside, r'class="recipe__card-sidebar-nutrition"', r"</aside>$") or aside
    flags, numeric, raw_lines = {}, [], []
    for lab, val in re.findall(r'recipe__card-sidebar-nutrition-list-label">(.*?)</span>(.*?)</li>',
                               aside, re.S):
        lab, val = clean(lab).rstrip(":"), clean(val) or ""
        raw_lines.append("%s: %s" % (lab, val))
        if val in ("✔", "✓", "✅"):
            flags[lab.lower()] = True
        elif val in ("𝙓", "X", "x", "✗", "✘", "❌"):
            flags[lab.lower()] = False
        else:
            numeric.append((lab, val))
    nut_note = re.search(r'recipe__card-sidebar-nutrition.*?<div class="rich-text">(.*?)</div>', aside, re.S)
    if nut_note:
        raw_lines.append(" ".join(paras(nut_note.group(1))))
    portions = meta.get("serving size") or meta.get("serves") or meta.get("servings")
    if portions:
        portions = re.sub(r"^serves\s*", "", portions, flags=re.I)

    # Ingredients
    ingredients = []
    ing_sec = between(body, r'class="recipe__ingredients"', r'class="recipe__card-steps"') or ""
    blocks = re.split(r'<div class="recipe__ingredients-block">', ing_sec)[1:]
    for b in blocks:
        g = re.search(r'recipe__ingredients-block__title[^>]*>(.*?)</h3>', b, re.S)
        group = clean(g.group(1)) if g else None
        bb = between(b, r'recipe__ingredients-block__body[^>]*>', r"</div>\s*$") or b
        bb = re.sub(r'<h3 class="recipe__ingredients-block__title.*?</h3>', "", bb, flags=re.S)
        for t in paras(bb):
            ingredients.append([group, t])
    if not blocks and ing_sec:
        for t in paras(re.sub(r"<h2.*?</h2>", "", ing_sec, flags=re.S)):
            ingredients.append([None, t])

    # Steps
    steps = []
    st_sec = between(body, r'class="recipe__card-steps"', r'(<section class="recipe__card-facts"|</article>)') or ""
    for li in re.findall(r'<li class="recipe__method-step">(.*?)</li>\s*(?=<li class="recipe__method-step">|</ol>)', st_sec, re.S):
        rt = re.search(r'<div class="rich-text">(.*)</div>', li, re.S)
        txt = paras(rt.group(1)) if rt else paras(re.sub(r"<h3.*?</h3>", "", li, flags=re.S))
        if txt:
            steps.append([None, " ".join(txt)])
    if not steps and st_sec:
        for t in paras(re.sub(r"<h2.*?</h2>", "", st_sec, flags=re.S)):
            steps.append([None, t])

    # Hints: chef quote + food-facts accordion + any other recipe__body sections
    hints = []
    quote = between(body, r'class="recipe__card-byline-quote"[^>]*>', r"</div>")
    if quote:
        q = " ".join(paras(quote))
        if q:
            hints.append(["Chef's note", q])
    facts = between(body, r'<section class="recipe__card-facts"', r"</section>") or ""
    for lab, sec in re.findall(r'data-name="accordion-trigger"[^>]*>(.*?)</button>\s*<div data-name="accordion-section"[^>]*>(.*?)</div>\s*</div>\s*(?=<div data-name="accordion-group"|</div>)', facts, re.S):
        txt = paras(sec)
        if txt:
            hints.append([clean(lab), "\n".join(txt)])
    if facts and not hints[1 if quote else 0:]:
        for t in paras(re.sub(r"<h2.*?</h2>", "", facts, flags=re.S)):
            hints.append([None, t])

    # Diet (only stated)
    diet = []
    if flags.get("low potassium") or "Low potassium" in tags:
        diet.append("Lower Potassium")
    if flags.get("low protein") or "Low protein" in tags:
        diet.append("Lower Protein")
    if flags.get("gluten-free") or flags.get("gluten free") or "Gluten-free" in tags:
        diet.append("Gluten-free")
    if flags.get("vegetarian") or flags.get("vegan") or "Vegetarian" in tags or "Vegan" in tags:
        diet.append("Vegetarian")
    alltext = " ".join([description or ""] + [h[1] for h in hints]).lower()
    if re.search(r"suitable for (people on |those on |anyone on |patients on )?(haemo|hemo|peritoneal )?dialysis", alltext):
        diet.append("Dialysis")
    if re.search(r"suitable for (people|those|anyone) (living )?with diabetes", alltext):
        diet.append("Diabetes")

    nutrients, unknown = parse_nutrients(numeric, portions)
    raw = "; ".join(raw_lines) if raw_lines else None

    course = [t for t in tags if t.lower() in ("breakfast", "christmas", "dessert", "lunch",
                                                "main meal", "snack", "special occasion")]
    ing_text = " ".join(i[1] for i in ingredients)
    steps_text = " ".join(s[1] for s in steps)
    category = pick_category(title, course, ing_text)

    dish = []
    tl = [t.lower() for t in tags]
    if "budget friendly" in tl or "budget-friendly" in tl:
        dish.append("Budget")
    if "quick and easy" in tl or "quick & easy" in tl:
        dish += ["Quick", "Easy"]
    if "15 minutes or less" in tl or "30 minutes or less" in tl:
        if "Quick" not in dish:
            dish.append("Quick")
    if "Vegetarian" in diet and category not in ("Desserts", "Beverages", "Breads",
                                                 "Sauces & Seasonings", "Breakfast & Brunch",
                                                 "Appetizers & Snacks", "Salads & Dressings") \
            and "main meal" in tl:
        dish.append("Meatless Entree")
    if re.search(r"\bsoup\b", title.lower()):
        dish.append("Soup")
    if re.search(r"\bstew\b", title.lower()):
        dish.append("Stew")
    if re.search(r"stir[- ]fry", title.lower()):
        dish.append("Stir-fry")
    if re.search(r"\bcake\b", title.lower()):
        dish.append("Cake")
    if re.search(r"\bmuffins?\b", title.lower()):
        dish.append("Muffin")
    if re.search(r"\b(cookies?|biscuits?)\b", title.lower()):
        dish.append("Cookies")
    if re.search(r"\bpie\b", title.lower()) and category == "Desserts":
        dish.append("Pie")
    if re.search(r"freez", " ".join(h[1] for h in hints if h[0] and "storage" in h[0].lower()).lower()) \
            and not re.search(r"(not|n't) (suitable for )?freez", alltext):
        dish.append("Freezer")
    if 0 < len(ingredients) <= 5:
        dish.append("5 or less ingredients")

    return {
        "source": KEY,
        "source_name": SOURCE_NAME,
        "source_id": slug,
        "url": url,
        "lang": "en",
        "title": title,
        "description": description,
        "image_url": image_url,
        "image_path": None,
        "portions": portions,
        "serving_size": None,
        "category": category,
        "diet": diet,
        "dish": dish,
        "cuisine": pick_cuisine(title),
        "method": pick_method(title, steps_text),
        "nutrients": nutrients,
        "nutrients_raw": raw,
        "ingredients": ingredients,
        "steps": steps,
        "hints": hints,
        "food_choices": [],
        "carb_choices": None,
        "video_url": None,
        "prep_time": meta.get("preparation time") or meta.get("prep time"),
        "cook_time": meta.get("cooking time") or meta.get("cook time"),
        "total_time": meta.get("total time"),
        "translation_of": None,
        "_tags": tags,
        "_unknown_nutrients": unknown,
        "_pdf": urljoin(BASE, pdf.group(1)) if pdf else None,
    }


def download_image(rec):
    if not rec.get("image_url"):
        return
    ext = os.path.splitext(urlparse(rec["image_url"]).path)[1].lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        ext = ".jpg"
    fn = rec["source_id"] + ext
    path = os.path.join(IMAGES, fn)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        st, data = fetch(rec["image_url"], binary=True)
        if data is None:
            print("  image failed", rec["image_url"], st, file=sys.stderr)
            return
        with open(path, "wb") as f:
            f.write(data)
    rec["image_path"] = "sources/%s/images/%s" % (KEY, fn)


# ---------------------------------------------------------------- main
def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(IMAGES, exist_ok=True)

    # 1. Recipe index, all pages
    index_slugs, index_pages = crawl_listing(INDEX)
    print("index: %d recipes over %d pages" % (len(index_slugs), index_pages))

    # 2. Filters: from the filter form and quick-filter links
    st, idx = fetch(INDEX)
    filters = set()
    for name, val in re.findall(r'name="([a-z]+_tags)"[^>]*value="([^"]+)"', idx):
        filters.add((name, val))
    for name, val in re.findall(r'quick-filter/([a-z_]+)/([a-z0-9-]+)/', idx):
        filters.add((name, val))
    filter_slugs, filter_counts = set(), {}
    for name, val in sorted(filters):
        s1, _ = crawl_listing(INDEX + "?%s=%s" % (name, val))
        u = set(s1)
        filter_counts["%s=%s" % (name, val)] = len(u)
        filter_slugs |= u
    print("filters: %d values, %d distinct recipes" % (len(filters), len(filter_slugs)))

    # 3. Collection / themed pages that link to recipes
    st, sm = fetch(SITEMAP)
    sm_urls = re.findall(r"<loc>([^<]+)</loc>", sm or "")
    sitemap_slugs = set()
    for u in sm_urls:
        m = RECIPE_RE.fullmatch(u)
        if m and m.group(1) not in NON_RECIPE_SLUGS:
            sitemap_slugs.add(m.group(1))
    collection_urls = [u for u in sm_urls if ("kidney-kitchen" in u and not RECIPE_RE.fullmatch(u))]
    collection_slugs = set()
    for u in collection_urls:
        st, body = fetch(u)
        if body:
            main_part = between(body, r"<main", r"</main>") or body
            collection_slugs |= set(recipe_links(main_part))
    print("sitemap: %d recipe-index URLs; collections: %d linked recipes" %
          (len(sitemap_slugs), len(collection_slugs)))

    all_slugs = sorted(set(index_slugs) | filter_slugs | sitemap_slugs | collection_slugs)

    # 4. Fetch recipe pages
    def get(slug):
        return slug, fetch(INDEX + slug + "/")
    with ThreadPoolExecutor(WORKERS) as ex:
        pages = list(ex.map(get, all_slugs))

    recipes, skipped = [], []
    for slug, (st, body) in pages:
        if body is None:
            skipped.append({"source_id": slug, "url": INDEX + slug + "/", "reason": "HTTP %s" % st})
            continue
        if re.search(r"cf-challenge|challenge-platform/h/|Just a moment\.\.\.", body[:5000]):
            skipped.append({"source_id": slug, "url": INDEX + slug + "/", "reason": "bot protection"})
            continue
        rec = parse_recipe(slug, body)
        if rec is None:
            skipped.append({"source_id": slug, "url": INDEX + slug + "/", "reason": "not a recipe page"})
            continue
        recipes.append(rec)

    with ThreadPoolExecutor(WORKERS) as ex:
        list(ex.map(download_image, recipes))

    unknown = sorted({u for r in recipes for u in r["_unknown_nutrients"]})
    for r in recipes:
        for k in ("_tags", "_unknown_nutrients", "_pdf"):
            r.pop(k, None)

    with open(os.path.join(HERE, "recipes.json"), "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, "skipped.json"), "w", encoding="utf-8") as f:
        json.dump(skipped, f, ensure_ascii=False, indent=1)

    idx_set = set(index_slugs)
    with_img = sum(1 for r in recipes if r["image_path"])
    with_nut = sum(1 for r in recipes if any(v is not None for v in r["nutrients"].values()))
    notes = [
        "Recipe index (all %d pages): %d recipes. Sitemap recipe-index URLs: %d. "
        "Filter listings (%d values) union: %d. Collection pages linked: %d. Union of all: %d."
        % (index_pages, len(idx_set), len(sitemap_slugs), len(filters), len(filter_slugs),
           len(collection_slugs), len(all_slugs)),
        "In sitemap not index: %s." % (sorted(sitemap_slugs - idx_set) or "none"),
        "In index not sitemap: %s." % (sorted(idx_set - sitemap_slugs) or "none"),
        "Only in filters/collections: %s." % (sorted((filter_slugs | collection_slugs) - idx_set - sitemap_slugs) or "none"),
        "Nutrition is per serving; the site gives only carbohydrate (g) and energy (kcal) numerically, "
        "plus dietitian-assessed yes/no flags (low potassium/phosphate/salt/fat/protein, high protein, "
        "vegetarian, vegan, gluten-free) and portion price, all kept in nutrients_raw. "
        "Diet mapped from ticked flags: Low potassium->Lower Potassium, Low protein->Lower Protein, "
        "Gluten-free, Vegetarian/Vegan->Vegetarian; Dialysis only if text says suitable for dialysis.",
        "Images are the largest srcset rendition (1050px wide) of the recipe hero photo.",
    ]
    if unknown:
        notes.append("Unmapped numeric nutrition labels kept in nutrients_raw: %s." % ", ".join(unknown))
    report = {"listed": len(idx_set), "scraped": len(recipes), "with_image": with_img,
              "with_nutrients": with_nut, "skipped": len(skipped), "notes": " ".join(notes)}
    with open(os.path.join(HERE, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
