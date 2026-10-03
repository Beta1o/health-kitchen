#!/usr/bin/env python3
"""Check a batch of healthy Saudi recipes: python3 sources/saudi/check.py <batch>"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
CATS = {"Appetizers & Snacks", "Beef, Lamb & Pork", "Beverages", "Breads", "Breakfast & Brunch", "Chicken & Turkey", "Desserts",
        "Fish & Seafood", "Pasta, Rice & Grains", "Pizza & Sandwiches", "Salads & Dressings", "Sauces & Seasonings", "Soups & Stews", "Vegetables"}
NK = ["calories", "protein_g", "carbohydrates_g", "fat_g", "cholesterol_mg", "sodium_mg", "potassium_mg", "phosphorus_mg", "calcium_mg", "fiber_g", "added_sugar_g"]
BAD = re.compile(r"\b(pork|bacon|ham|gelatin|wine|beer|rum|brandy|champagne|liqueur|lard)\b|خنزير|جيلاتين|نبيذ|شمبانيا|شامبين|كحول", re.I)
recs = json.load(open(HERE / "out" / f"{sys.argv[1]}.json", encoding="utf-8"))
errs = []
by = {}
for r in recs:
    sid = r.get("source_id", "?")
    by[sid] = r
    for k in ("source", "source_name", "source_id", "url", "lang", "title", "description", "portions", "serving_size", "category", "ingredients", "steps", "hints", "nutrients"):
        if not r.get(k):
            errs.append(f"{sid}: missing {k}")
    if r.get("category") not in CATS: errs.append(f"{sid}: bad category {r.get('category')}")
    if r.get("cuisine") != ["Saudi"]: errs.append(f"{sid}: cuisine must be ['Saudi']")
    n = r.get("nutrients") or {}
    for k in NK:
        if not isinstance(n.get(k), (int, float)): errs.append(f"{sid}: nutrient {k} missing")
    if isinstance(n.get("calories"), (int, float)) and not 20 <= n["calories"] <= 1100: errs.append(f"{sid}: calories {n['calories']} out of range")
    if isinstance(n.get("sodium_mg"), (int, float)) and n["sodium_mg"] > 900: errs.append(f"{sid}: sodium {n['sodium_mg']} mg too high for a healthy recipe")
    txt = json.dumps([r.get("title"), r.get("ingredients"), r.get("steps"), r.get("hints")], ensure_ascii=False)
    if BAD.search(txt): errs.append(f"{sid}: excluded ingredient/word: {BAD.search(txt).group()}")
    if re.search(r"\b(cups?|oz|ounces?|lbs?|pounds?|°F)\b", txt, re.I): errs.append(f"{sid}: non-metric unit")
    if r.get("lang") == "ar" and not (HERE / "calc" / f"{sid}.json").exists(): errs.append(f"{sid}: calc file missing")
for sid, r in by.items():
    if r["lang"] == "en":
        a = by.get(r.get("translation_of"))
        if not a: errs.append(f"{sid}: no Arabic record {r.get('translation_of')}"); continue
        for k in ("ingredients", "steps", "hints"):
            if len(a[k]) != len(r[k]): errs.append(f"{sid}: {k} count differs from Arabic ({len(a[k])} vs {len(r[k])})")
        if a["nutrients"] != r["nutrients"]: errs.append(f"{sid}: nutrients differ from Arabic")
print("\n".join(errs) if errs else f"OK ({len(recs)} records)")
