#!/usr/bin/env python3
"""Nutrition from USDA FoodData Central, SR Legacy (nutrition/sr.zip, public domain).

  python3 nutrition/usda.py build                       # once: sr.zip -> nutrition/usda.db
  python3 nutrition/usda.py search rice white cooked    # find foods (fdc id, description)
  python3 nutrition/usda.py show 168878                 # nutrients per 100 g of one food
  python3 nutrition/usda.py calc recipe.json            # per-serving nutrients of a recipe

recipe.json: {"servings": 4, "items": [{"fdc": 168878, "g": 300}, {"fdc": 169655, "g": 20, "added_sugar": true}, ...]}
Weights are the edible amount as eaten in the dish (raw weight for raw-listed foods, cooked
weight for cooked-listed foods). Lines marked added_sugar count their total sugars as added sugar
(sugar, honey, date syrup, molasses). Water and other zero-nutrient items can be left out.
"""
import csv
import io
import json
import sqlite3
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE / "usda.db"
ZIP = HERE / "sr.zip"
# app column -> SR Legacy nutrient id
NUTR = {"calories": 1008, "protein_g": 1003, "carbohydrates_g": 1005, "fat_g": 1004, "cholesterol_mg": 1253,
        "sodium_mg": 1093, "potassium_mg": 1092, "phosphorus_mg": 1091, "calcium_mg": 1087, "fiber_g": 1079,
        "sugars_g": 2000}


def build():
    z = zipfile.ZipFile(ZIP)
    root = "FoodData_Central_sr_legacy_food_csv_2018-04/"
    read = lambda n: csv.DictReader(io.TextIOWrapper(z.open(root + n), encoding="utf-8"))
    db = sqlite3.connect(DB)
    db.executescript("DROP TABLE IF EXISTS food; DROP TABLE IF EXISTS nut;"
                     "CREATE TABLE food (fdc INTEGER PRIMARY KEY, name TEXT);"
                     "CREATE TABLE nut (fdc INTEGER, k TEXT, v REAL, PRIMARY KEY (fdc, k));")
    db.executemany("INSERT INTO food VALUES (?, ?)", ((int(r["fdc_id"]), r["description"]) for r in read("food.csv")))
    rev = {v: k for k, v in NUTR.items()}
    db.executemany("INSERT OR REPLACE INTO nut VALUES (?, ?, ?)",
                   ((int(r["fdc_id"]), rev[int(r["nutrient_id"])], float(r["amount"]))
                    for r in read("food_nutrient.csv") if int(r["nutrient_id"]) in rev and r["amount"]))
    db.commit()
    print(db.execute("SELECT count(*) FROM food").fetchone()[0], "foods")


def con():
    if not DB.exists():
        build()
    return sqlite3.connect(DB)


def search(words):
    db = con()
    q = "SELECT fdc, name FROM food WHERE " + " AND ".join("name LIKE ?" for _ in words) + " ORDER BY length(name) LIMIT 25"
    for fdc, name in db.execute(q, [f"%{w}%" for w in words]):
        print(fdc, name)


def per100(db, fdc):
    return {k: v for k, v in db.execute("SELECT k, v FROM nut WHERE fdc = ?", (fdc,))}


def calc(recipe):
    db = con()
    tot = {k: 0.0 for k in NUTR}
    added = 0.0
    missing = []
    for it in recipe["items"]:
        n = per100(db, it["fdc"])
        if not n:
            missing.append(it["fdc"])
            continue
        f = it["g"] / 100
        for k in NUTR:
            tot[k] += n.get(k, 0) * f
        if it.get("added_sugar"):
            added += n.get("sugars_g", 0) * f
    sv = recipe["servings"]
    out = {k: round(v / sv, 1) for k, v in tot.items() if k != "sugars_g"}
    for k in ("calories", "cholesterol_mg", "sodium_mg", "potassium_mg", "phosphorus_mg", "calcium_mg"):
        out[k] = round(out[k])
    out["added_sugar_g"] = round(added / sv, 1)
    if missing:
        out["missing_fdc"] = missing
    return out


if __name__ == "__main__":
    cmd, *args = sys.argv[1:] or ["help"]
    if cmd == "build":
        build()
    elif cmd == "search":
        search(args)
    elif cmd == "show":
        db = con()
        print(db.execute("SELECT name FROM food WHERE fdc = ?", (int(args[0]),)).fetchone(), per100(db, int(args[0])))
    elif cmd == "calc":
        print(json.dumps(calc(json.load(open(args[0], encoding="utf-8"))), ensure_ascii=False))
    else:
        print(__doc__)
