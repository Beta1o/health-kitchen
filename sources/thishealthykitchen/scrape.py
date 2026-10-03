#!/usr/bin/env python3
"""Scrape every recipe published by This Healthy Kitchen (thishealthykitchen.com).

Discovery: the WordPress REST API lists every post (wp-json/wp/v2/posts); each post
page is fetched and its schema.org Recipe (JSON-LD) is read for title, yield,
ingredients, steps, nutrition and photo. Ingredient groups and notes come from the
WP Recipe Maker card in the page. Posts without a Recipe (round-ups, guides) are
skipped and listed in skipped.json. Output follows sources/FORMAT.md.
Re-runnable: pages are cached under cache/, images already on disk are kept.
robots.txt allows everything outside /wp-admin/.
"""
import hashlib
import html
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

import requests

KEY = "thishealthykitchen"
SOURCE_NAME = "This Healthy Kitchen"
BASE = "https://thishealthykitchen.com"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
IMAGES = os.path.join(HERE, "images")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
S = requests.Session()
S.headers["User-Agent"] = UA


def get(url, binary=False, tries=5):
    for i in range(tries):
        try:
            r = S.get(url, timeout=40)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 ** i + 1)
                continue
            r.raise_for_status()
            return r.content if binary else r.text
        except requests.RequestException:
            if i == tries - 1:
                raise
            time.sleep(2 ** i + 1)


def cached(url):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, hashlib.md5(url.encode()).hexdigest() + ".html")
    if os.path.exists(p):
        return open(p, encoding="utf-8").read()
    t = get(url)
    open(p, "w", encoding="utf-8").write(t)
    time.sleep(0.4)
    return t


def list_posts():
    posts, page = [], 1
    while True:
        r = S.get(f"{BASE}/wp-json/wp/v2/posts", params={"per_page": 100, "page": page, "_fields": "id,slug,link,title"}, timeout=40)
        if r.status_code == 400:
            break
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        posts += batch
        if page >= int(r.headers.get("X-WP-TotalPages", page)):
            break
        page += 1
    return posts, int(r.headers.get("X-WP-Total", len(posts)))


def text(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def find_recipe(page):
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', page, re.S):
        try:
            d = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        items = d.get("@graph", [d]) if isinstance(d, dict) else d
        for x in items:
            t = x.get("@type")
            if t == "Recipe" or (isinstance(t, list) and "Recipe" in t):
                return x
    return None


def num(v):
    m = re.search(r"[\d.]+", str(v or ""))
    return float(m.group()) if m else None


def steps_of(ins):
    out = []
    for s in ins or []:
        if isinstance(s, str):
            out.append([None, text(s)])
        elif s.get("@type") == "HowToSection":
            for x in s.get("itemListElement", []):
                out.append([text(s.get("name")) or None, text(x.get("text"))])
        else:
            out.append([None, text(s.get("text"))])
    return [x for x in out if x[1]]


def ingredient_groups(page, flat):
    """[[group label or None, text]] from the WPRM card; falls back to the JSON-LD list."""
    card = page.find("wprm-recipe-ingredient-group")
    if card < 0:
        return [[None, text(x)] for x in flat]
    out = []
    for g in re.finditer(r'<div class="wprm-recipe-ingredient-group">(.*?)</ul>', page, re.S):
        h = re.search(r'wprm-recipe-group-name[^>]*>(.*?)</', g.group(1), re.S)
        label = text(h.group(1)) if h else None
        for li in re.finditer(r'<li class="wprm-recipe-ingredient"[^>]*>(.*?)</li>', g.group(1), re.S):
            t = text(li.group(1)).replace(" ▢", "").lstrip("▢ ").strip()
            if t:
                out.append([label or None, t])
    return out or [[None, text(x)] for x in flat]


def notes_of(page):
    m = re.search(r'<div class="wprm-recipe-notes"[^>]*>(.*?)</div>\s*</div>', page, re.S)
    if not m:
        return []
    parts = re.split(r"</p>|<br\s*/?>|</li>", m.group(1))
    return [[None, t] for t in (text(p) for p in parts) if len(t) > 3]


CATS = [  # (category, words in title / keywords / recipeCategory)
    ("Beverages", r"smoothie|latte|tea\b|lemonade|juice|drink|mocktail|coffee|shake"),
    ("Desserts", r"dessert|cake|cookie|brownie|muffin|pudding|bliss ball|energy ball|bar\b|bars\b|pie\b|crumble|ice cream|fudge|truffle|sweet"),
    ("Breakfast & Brunch", r"breakfast|oat|granola|pancake|waffle|porridge|overnight|egg muffin|frittata|chia"),
    ("Soups & Stews", r"soup|stew|chili|chowder|broth|curry"),
    ("Salads & Dressings", r"salad|dressing|vinaigrette|slaw"),
    ("Sauces & Seasonings", r"sauce|dip\b|hummus|pesto|seasoning|spice blend|salsa|guacamole|jam\b|butter\b"),
    ("Breads", r"bread|loaf|scone|flatbread|bagel|roll\b|rolls\b|biscuit"),
    ("Pizza & Sandwiches", r"pizza|sandwich|wrap|burger|taco|quesadilla|toast"),
    ("Fish & Seafood", r"salmon|fish|shrimp|tuna|cod\b|prawn|seafood|tilapia"),
    ("Chicken & Turkey", r"chicken|turkey"),
    ("Beef, Lamb & Pork", r"beef|lamb|steak|meatball|mince"),
    ("Pasta, Rice & Grains", r"pasta|rice|quinoa|noodle|couscous|risotto|orzo|grain|bowl"),
    ("Appetizers & Snacks", r"snack|bites|appetizer|chips|crackers|popcorn|nuts|roasted chickpea|fries"),
    ("Vegetables", r"vegetable|veggie|broccoli|cauliflower|potato|squash|zucchini|carrot|bean|lentil|tofu|mushroom|spinach|kale|eggplant"),
]


def category(title, kw, rc):
    hay = f"{title} {kw} {' '.join(rc)}".lower()
    for c, rx in CATS:
        if re.search(rx, title.lower()):
            return c
    for c, rx in CATS:
        if re.search(rx, hay):
            return c
    return "Vegetables"


def main():
    os.makedirs(IMAGES, exist_ok=True)
    posts, total = list_posts()
    print("posts listed:", total, len(posts))

    def one(p):
        try:
            return p, cached(p["link"])
        except Exception as e:  # noqa: BLE001
            return p, e

    with ThreadPoolExecutor(3) as ex:
        pages = list(ex.map(one, posts))
    recipes, skipped = [], []
    for p, page in pages:
        if isinstance(page, Exception):
            skipped.append({"url": p["link"], "reason": str(page)})
            continue
        r = find_recipe(page)
        if not r or not r.get("recipeIngredient"):
            skipped.append({"url": p["link"], "reason": "no recipe card"})
            continue
        n = r.get("nutrition") or {}
        kw = r.get("keywords") or ""
        rc = r.get("recipeCategory") or []
        rc = rc if isinstance(rc, list) else [rc]
        cu = r.get("recipeCuisine") or []
        cu = [c for c in (cu if isinstance(cu, list) else [cu]) if c and c != "Not Specified"]
        y = r.get("recipeYield")
        y = y if isinstance(y, list) else [y]
        portions = str(y[-1]) if y and y[-1] else None
        img = r.get("image")
        img = (img[0] if isinstance(img, list) else img.get("url") if isinstance(img, dict) else img) or None
        sid = p["slug"]
        img_path = None
        if img:
            rel = f"sources/{KEY}/images/{sid}.jpg"
            dst = os.path.join(IMAGES, f"{sid}.jpg")
            if not os.path.exists(dst):
                try:
                    open(dst, "wb").write(get(img, binary=True))
                except Exception:  # noqa: BLE001
                    dst = None
            img_path = rel if dst else None
        diet = []
        low = (kw + " " + " ".join(rc) + " " + r.get("name", "")).lower()
        if "gluten-free" in low or "gluten free" in low:
            diet.append("Gluten-free")
        if "vegan" in low or "vegetarian" in low:
            diet.append("Vegetarian")
        recipes.append({
            "source": KEY, "source_name": SOURCE_NAME, "source_id": sid, "url": p["link"], "lang": "en",
            "title": text(r.get("name")), "description": text(r.get("description")) or None,
            "image_url": img, "image_path": img_path,
            "portions": portions, "serving_size": text(n.get("servingSize")) or None,
            "category": category(text(r.get("name")), kw, rc), "diet": diet, "dish": [], "cuisine": cu, "method": [],
            "nutrients": {"calories": num(n.get("calories")), "protein_g": num(n.get("proteinContent")),
                          "carbohydrates_g": num(n.get("carbohydrateContent")), "fat_g": num(n.get("fatContent")),
                          "cholesterol_mg": num(n.get("cholesterolContent")), "sodium_mg": num(n.get("sodiumContent")),
                          "potassium_mg": num(n.get("potassiumContent")), "phosphorus_mg": None, "calcium_mg": num(n.get("calciumContent")),
                          "fiber_g": num(n.get("fiberContent")), "added_sugar_g": None},
            "nutrients_raw": json.dumps(n, ensure_ascii=False) if n else None,
            "ingredients": ingredient_groups(page, r.get("recipeIngredient") or []),
            "steps": steps_of(r.get("recipeInstructions")), "hints": notes_of(page), "food_choices": [],
            "carb_choices": None, "video_url": None,
            "prep_time": r.get("prepTime"), "cook_time": r.get("cookTime"), "total_time": r.get("totalTime"),
            "translation_of": None,
        })
    json.dump(recipes, open(os.path.join(HERE, "recipes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(skipped, open(os.path.join(HERE, "skipped.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rep = {"listed": total, "scraped": len(recipes), "with_image": sum(1 for x in recipes if x["image_path"]),
           "with_nutrients": sum(1 for x in recipes if x["nutrients"]["calories"] is not None), "skipped": len(skipped),
           "notes": "Posts without a schema.org Recipe (round-ups, guides) are skipped. Total sugar is not stored as added sugar."}
    json.dump(rep, open(os.path.join(HERE, "report.json"), "w"), indent=1)
    print(rep)


if __name__ == "__main__":
    main()
