#!/usr/bin/env python3
"""Load the external recipe sources (sources/<key>/recipes.json, see sources/FORMAT.md)
into davita_recipes.db next to the DaVita recipes, and add davita.sa photos to
matching DaVita recipes that have none.

Run after scrape_davita.py (which recreates the base tables) and before
halal_filter.py / i18n.py. Re-runnable: it replaces earlier imports of each source.

Usage: python3 import_sources.py
"""
import json
import re
import sqlite3
from pathlib import Path

from terms_i18n import TERMS

HERE = Path(__file__).resolve().parent
DB = HERE / "davita_recipes.db"
SRC = HERE / "sources"
# id ranges keep ids stable and unique per source
OFFSETS = {"davita_sa": 2_000_000, "kidneycareuk": 3_000_000, "aakp": 4_000_000, "myrenalnutrition": 5_000_000}
TAX = {"diet": "diet_type", "dish": "dish_type", "cuisine": "cuisine", "method": "cooking_method"}
NUTRIENTS = ["calories", "protein_g", "carbohydrates_g", "fat_g", "cholesterol_mg", "sodium_mg",
             "potassium_mg", "phosphorus_mg", "calcium_mg", "fiber_g", "added_sugar_g"]
CATEGORIES = [k for k in TERMS if k in {
    "Appetizers & Snacks", "Beef, Lamb & Pork", "Beverages", "Breads", "Breakfast & Brunch", "Chicken & Turkey",
    "Desserts", "Fish & Seafood", "Pasta, Rice & Grains", "Pizza & Sandwiches", "Salads & Dressings",
    "Sauces & Seasonings", "Soups & Stews", "Vegetables"}]


def num(v):
    try:
        return float(v) if v is not None and v != "" else None
    except (TypeError, ValueError):
        return None


def stable_index(source_id):
    """Deterministic small number from a source id (keeps recipe ids stable across runs)."""
    h = 0
    for ch in source_id:
        h = (h * 131 + ord(ch)) % 999_983
    return h


def main():
    db = sqlite3.connect(DB)
    cols = {r[1] for r in db.execute("PRAGMA table_info(recipes)")}
    for c, t in (("canonical_id", "INTEGER"), ("source_name", "TEXT")):
        if c not in cols:
            db.execute(f"ALTER TABLE recipes ADD COLUMN {c} {t}")
    db.execute("UPDATE recipes SET source_name='DaVita' WHERE site IN ('davita.com','espanol.davita.com')")

    # terms: reuse the English DaVita term rows by name, create the rest
    term_id = {(t, n): i for i, t, n in db.execute("SELECT id, taxonomy, name FROM terms WHERE site='davita.com'")}
    next_term = (db.execute("SELECT max(id) FROM terms WHERE id >= 9000000").fetchone()[0] or 9_000_000) + 1

    def term(tax, name):
        nonlocal next_term
        key = (tax, name)
        if key not in term_id:
            db.execute("INSERT INTO terms VALUES (?,?,?,?,?,?)", (next_term, "external", tax, name, None, None))
            term_id[key] = next_term
            next_term += 1
        return term_id[key]

    total = 0
    for key, off in OFFSETS.items():
        path = SRC / key / "recipes.json"
        if not path.exists():
            continue
        recs = json.loads(path.read_text(encoding="utf-8"))
        # forget earlier import of this source
        old = [r for (r,) in db.execute("SELECT id FROM recipes WHERE site=?", (key,))]
        tables = ["ingredients", "steps", "hints", "food_choices", "recipe_terms"]
        tables += [t for (t,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%_i18n'")]
        for t in tables:
            db.executemany(f"DELETE FROM {t} WHERE recipe_id=?", [(r,) for r in old])
        db.execute("DELETE FROM recipes WHERE site=?", (key,))

        ids, used = {}, set()
        for r in sorted(recs, key=lambda r: (r.get("translation_of") is not None, r["source_id"], r["lang"])):
            idx = stable_index(f'{r["source_id"]}|{r["lang"]}')
            while off + idx in used:
                idx = (idx + 1) % 999_983
            rid = off + idx
            used.add(rid)
            ids[(r["source_id"], r["lang"])] = rid
        primary = {r["source_id"]: ids[(r["source_id"], r["lang"])] for r in recs if not r.get("translation_of")}

        for r in recs:
            rid = ids[(r["source_id"], r["lang"])]
            canon = primary.get(r.get("translation_of") or r["source_id"], rid)
            cat = r.get("category") if r.get("category") in CATEGORIES else "Vegetables"
            n = r.get("nutrients") or {}
            row = {
                "id": rid, "site": key, "language": r["lang"], "wp_id": idx_of(rid, off), "slug": r["source_id"],
                "title": r["title"], "url": r["url"] if r["lang"] == "en" or not r.get("translation_of") else r["url"] + f"#{r['lang']}",
                "category": cat, "category_en": cat, "description": r.get("description"),
                "image_url": r.get("image_url"), "image_path": r.get("image_path") if r.get("image_path") and (HERE / r["image_path"]).exists() else None,
                "portions": r.get("portions"), "serving_size": r.get("serving_size"),
                "carbohydrate_choices": r.get("carb_choices"), "nutrition_footnote": None,
                "prep_time": r.get("prep_time"), "cook_time": r.get("cook_time"), "total_time": r.get("total_time"),
                "video_url": r.get("video_url"), "meta_json": json.dumps(r, ensure_ascii=False),
                "canonical_id": canon, "source_name": r.get("source_name") or key,
            }
            for c in NUTRIENTS:
                row[c] = num(n.get(c))
                row[c + "_raw"] = None if n.get(c) is None else str(n.get(c))
            names = ", ".join(row)
            db.execute(f"INSERT INTO recipes ({names}) VALUES ({','.join('?' * len(row))})", list(row.values()))
            for t, field in (("ingredients", "ingredients"), ("steps", "steps"), ("hints", "hints")):
                db.executemany(f"INSERT INTO {t} VALUES (?,?,?,?)",
                               [(rid, i, g, x) for i, (g, x) in enumerate(r.get(field) or [], 1) if x])
            db.executemany("INSERT INTO food_choices VALUES (?,?,?)",
                           [(rid, i, x) for i, x in enumerate(r.get("food_choices") or [], 1) if x])
            if canon == rid:
                db.execute("INSERT OR IGNORE INTO recipe_terms VALUES (?,?,?)", (rid, term("category", cat), "category"))
                for f, tax in TAX.items():
                    for v in r.get(f) or []:
                        db.execute("INSERT OR IGNORE INTO recipe_terms VALUES (?,?,?)", (rid, term(tax, v), tax))
        print(f"{key}: {len(recs)} records, {len(primary)} recipes")
        total += len(primary)

    # davita.sa photos for DaVita recipes that have none
    mpath = SRC / "davita_sa" / "matches.json"
    added = 0
    if mpath.exists():
        for m in json.loads(mpath.read_text(encoding="utf-8")):
            if m.get("image_path") and (HERE / m["image_path"]).exists():
                added += db.execute("UPDATE recipes SET image_path=?, image_url=? WHERE id=? AND image_path IS NULL",
                                    (m["image_path"], m["image_url"], m["db_recipe_id"])).rowcount
    db.commit()
    print(f"imported {total} external recipes; davita.sa photos added to {added} DaVita recipes")


def idx_of(rid, off):
    return rid - off


if __name__ == "__main__":
    main()
