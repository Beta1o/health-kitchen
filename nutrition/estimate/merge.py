#!/usr/bin/env python3
"""Fill nutrients a publisher does not print (potassium, phosphorus, calcium, cholesterol, added sugar) from the
ingredient-list calculation in nutrition/estimate/calc/<id>.json (USDA SR Legacy, see GUIDE.md).

An estimate is only used when the calculation reproduces what the publisher did print: calories and at least one
of protein and carbohydrate are published, and each published one agrees within 25% (or a small absolute amount
for low values). Sodium is not part of the check: it mostly reflects how much salt "to taste" is counted, not
whether the foods and amounts are right. A calculation off by one consistent factor (a different serving count) is
scaled to the publisher's servings (rescaled()).
A second blind calculation of the recipes that fail was tried (2026-10-15) and not used: on ADA recipes that publish
potassium, the retries that passed were within 30% only 63% of the time (first pass 83%), so retrying until a
calculation passes lets worse estimates through. Published numbers are never replaced. Estimated nutrients are listed in rec["e"] (their index),
so the app marks them "≈" and the diet tags keep a safety margin (diet_tags.py).

A blind test on 40 recipes with published values (DaVita and ADA) found that, when this check passes,
potassium was within 30% for 29 of 32 recipes and phosphorus for 18 of 21; the larger misses were overestimates.

  python3 nutrition/estimate/merge.py      # report only: how many recipes pass the check
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import usda   # noqa: E402

CALC = HERE / "calc"
# build_gallery.NUTRIENTS order
KEYS = ["calories", "protein_g", "carbohydrates_g", "fat_g", "cholesterol_mg", "sodium_mg",
        "potassium_mg", "phosphorus_mg", "calcium_mg", "fiber_g", "added_sugar_g"]
FILL = [4, 6, 7, 8, 10]                                  # nutrients an estimate may fill
CHECK = {0: 30, 1: 3, 2: 4}                              # index -> absolute tolerance; plus 25% relative
REL = 0.25
# salt substitutes and sodium-free stock are potassium chloride, which the calculation leaves out
KCL = re.compile(r"salt substitute|potassium chloride|\bno ?salt\b(?! added)|\blo-?salt\b|\bnu-?salt\b|"
                 r"sodium[- ]free (bouillon|stock|broth)|salt[- ]free (bouillon|stock cube)", re.I)


def agrees(calc, pub):
    shown = [i for i in CHECK if pub[i] is not None]
    if pub[0] is None or len(shown) < 2:
        return False
    return all(abs(calc[i] - pub[i]) <= max(CHECK[i], REL * pub[i]) for i in shown)


def rescaled(calc, pub):
    """When calories, protein and carbohydrate are all off by the same factor (within 30% of each other), the foods
    are right and the serving count differs from the publisher's: scale by that factor and check again.
    Checked on 116 ADA recipes that publish potassium: 78% within 30%."""
    rat = sorted(pub[i] / calc[i] for i in CHECK if pub[i] and calc[i] and pub[i] >= (20 if i == 0 else 3))
    if pub[0] is None or len(rat) < 2 or rat[-1] / rat[0] > 1.3:
        return None
    f = rat[len(rat) // 2]
    out = [v * f if v is not None else None for v in calc]
    return [round(v) if v is not None and i in (4, 6, 7, 8) else (round(v, 1) if v is not None else None)
            for i, v in enumerate(out)] if agrees(out, pub) else None


def known(spec, key):
    """USDA lists no value for some foods (e.g. soy yogurt has no potassium); the calculation would count them as 0,
    so a nutrient is only estimated when foods with a value make up at least 90% of the recipe's weight."""
    db = usda.con()
    items = [it for it in spec["items"] if it.get("added_sugar")] if key == "sugars_g" else spec["items"]
    gap = sum(it["g"] for it in items
              if not db.execute("SELECT 1 FROM nut WHERE fdc = ? AND k = ?", (it["fdc"], key)).fetchone())
    return gap / (sum(it["g"] for it in items) or 1) <= 0.10


def fill(recipes):
    """Fill missing nutrients in rec["n"] in place; return a report."""
    rep = {"calc_files": 0, "passed": 0, "failed": [], "rescaled": [], "kcl": [], "pub_lowk": [], "filled": {k: 0 for k in (KEYS[i] for i in FILL)}}
    for rec in recipes:
        f = CALC / f"{rec['id']}.json"
        if not f.exists():
            continue
        rep["calc_files"] += 1
        spec = json.loads(f.read_text(encoding="utf-8"))
        c = usda.calc(spec)
        calc = [c.get(k) for k in KEYS]
        n = rec["n"]
        if not agrees(calc, n):
            calc = rescaled(calc, n)
            if not calc:
                rep["failed"].append(rec["id"])
                continue
            rep["rescaled"].append(rec["id"])
        est = [i for i in FILL if n[i] is None and calc[i] is not None and known(spec, "sugars_g" if i == 10 else KEYS[i])]
        if "Lower Potassium" in rec["diet"]:
            # kidney publishers count potassium after leaching (boiled, drained vegetables), which raw USDA values do not
            est = [i for i in est if i != 6]
            rep["pub_lowk"].append(rec["id"])
        if KCL.search(" ".join(x[1] for x in (rec["t"].get("en") or {}).get("ing", []))):
            est = [i for i in est if i != 6]     # potassium chloride is not in the calculation: no potassium estimate
            rep["kcl"].append(rec["id"])
        if not est:
            continue
        rep["passed"] += 1
        for i in est:
            n[i] = calc[i]
            rep["filled"][KEYS[i]] += 1
        rec["e"] = est
    return rep


if __name__ == "__main__":
    src = (HERE.parent.parent / "gallery" / "data.js").read_text(encoding="utf-8")
    recs = json.loads(src[src.index("{"):src.rindex("}") + 1])["recipes"]
    for r in recs:   # undo earlier estimates so the report starts from the published numbers
        for i in r.get("e", []):
            r["n"][i] = None
    rep = fill(recs)
    print({k: (len(v) if isinstance(v, list) else v) for k, v in rep.items()})
