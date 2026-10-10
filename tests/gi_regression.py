#!/usr/bin/env python3
"""Regression check for the glycemic estimates: 20 fixed recipes and their carbohydrate, potassium, GI and GL.

  python3 tests/gi_regression.py            # compare with tests/gi_snapshot.json (exit 1 on any change)
  python3 tests/gi_regression.py --update   # accept the current values after a deliberate change

The snapshot holds the app's own computed values, so it catches unintended changes; it is not a clinical
reference. Recipes are looked up by title so the check survives a rebuild of the database.
"""
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import glycemic  # noqa: E402

TITLES = ["Savory White Rice", "Basmati Summer Salad", "Curried Lentil Soup", "Lentil Soup with California Dates and Spinach",
          "Lemon Pound Cake", "Maple Pancakes", "Mixed Berry and Basil Fruit Salad", "Baked Potato, small", "Air Fryer Sweet Potato Cubes",
          "Chicken Fruit Salad", "Palacsinta (Dessert Pancakes)", "Cottage Cheese Pancakes with Fresh Strawberries", "Fruit Salad Slaw",
          "Mediterranean Lentil Soup", "Roast butternut squash and red lentil soup", "Zucchini-Onion Latkes (Pancakes)", "Creamy Fruit Salad",
          "Baby baked potatoes with beef and horseradish", "Spicy Peaches", "Tuna Koko Sandwich"]
SNAP = HERE / "gi_snapshot.json"


def current():
    db = sqlite3.connect(os.environ.get("HK_DB") or HERE.parent / "davita_recipes.db")
    out = {}
    for t in TITLES:
        row = db.execute("SELECT id, portions, carbohydrates_g, fiber_g, potassium_mg, coalesce(source_name, 'DaVita') FROM recipes "
                         "WHERE title = ? AND canonical_id = id", (t,)).fetchone()
        if not row:
            out[t] = None
            continue
        rid, por, carbs, fiber, k, src = row
        lines = [x for (x,) in db.execute("SELECT text FROM ingredients_i18n WHERE recipe_id=? AND lang='en' ORDER BY position", (rid,))]
        m = re.match(r"\s*(\d+)", por or "")
        res, _ = glycemic.recipe(lines, int(m.group(1)) if m else None, carbs, fiber, src, por)
        res = res or {}
        out[t] = {"carbs_g": carbs, "potassium_mg": k, "gi": res.get("gi"), "gl": res.get("gl")}
    return out


def main():
    now = current()
    if "--update" in sys.argv or not SNAP.exists():
        SNAP.write_text(json.dumps(now, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"snapshot written: {len(now)} recipes")
        return 0
    old = json.loads(SNAP.read_text(encoding="utf-8"))
    diffs = [(t, old.get(t), now.get(t)) for t in TITLES if old.get(t) != now.get(t)]
    for t, a, b in diffs:
        print(f"CHANGED {t}: {a} -> {b}")
    print(f"gi regression: {len(TITLES) - len(diffs)}/{len(TITLES)} unchanged")
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
