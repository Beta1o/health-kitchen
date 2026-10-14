#!/usr/bin/env python3
"""Diet-type tags worked out from a recipe's published nutrition per serving.

Publishers tag recipes inconsistently (Diabetes UK never marks kidney diets, Kidney Care UK marks every recipe
"Lower Potassium", This Healthy Kitchen has no diabetes tag), so every recipe whose numbers are known gets the
same rules. Publisher tags are kept; tags the numbers contradict are listed in the report for a dietitian.

A nutrient that is neither published nor estimated never passes a rule. Estimated values (nutrition/estimate,
marked "≈" in the app) must clear each limit by 15%.

Limits per serving (one meal is about a third of the day):
  Lower Potassium   potassium <= 200 mg                      (app quick pick and colour level)
  Higher Potassium  potassium > 400 mg                       (app colour level)
  Lower Protein     protein <= 10 g                          (app quick pick)
  CKD non-dialysis  protein <= 20 g, potassium <= 400 mg, phosphorus <= 250 mg, sodium <= 600 mg
  Dialysis          potassium <= 600 mg, phosphorus <= 350 mg, sodium <= 800 mg
  Diabetes          carbohydrate <= 45 g, added sugar <= 6 g when published, glycemic load not high (<= 19)
Heart Healthy is not derived: publishers give it to few recipes on grounds the numbers don't show (no rule on
sodium, cholesterol and fat matched DaVita's or ADA's choices), and saturated fat is not published. The
"Heart-healthy" quick pick filters by the numbers instead.
The CKD and dialysis limits were set against the tags DaVita and AAKP dietitians gave their own recipes
(83% and 94% agreement, 94% and 97% of tagged recipes meet them). The build prints the agreement each time
and writes diet_tags_report.json: tags added per source and the publisher tags the numbers contradict.
"""
# index in the recipe nutrient list (build_gallery.NUTRIENTS)
KCAL, PROT, CARB, FAT, CHOL, NA, K, P, CA, FIB, SUG = range(11)


def _le(v, m):
    return v is not None and v <= m


# estimated values (nutrition/estimate) must clear a limit by 15%; published values are used as printed
MARGIN = 0.85


RULES = {
    "Lower Potassium": lambda n, gl: _le(n[K], 200),
    "Higher Potassium": lambda n, gl: n[K] is not None and n[K] > 400,
    "Lower Protein": lambda n, gl: _le(n[PROT], 10),
    "CKD non-dialysis": lambda n, gl: _le(n[PROT], 20) and _le(n[K], 400) and _le(n[P], 250) and _le(n[NA], 600),
    "Dialysis": lambda n, gl: _le(n[K], 600) and _le(n[P], 350) and _le(n[NA], 800),
    "Diabetes": lambda n, gl: _le(n[CARB], 45) and (n[SUG] is None or n[SUG] <= 6) and not (gl is not None and gl > 19),
}
# what a rule needs before it can say "no" (a publisher tag on a recipe without these numbers is not a conflict)
NEEDS = {"Lower Potassium": [K], "Higher Potassium": [K], "Lower Protein": [PROT], "CKD non-dialysis": [PROT, K, P, NA],
         "Dialysis": [K, P, NA], "Diabetes": [CARB]}


def derive(n, gl, est=()):
    """Tags the numbers support. Estimated nutrients count at 1/MARGIN of their value for upper limits
    (and at MARGIN for "Higher Potassium"), so a tag never rests on an estimate close to the line."""
    if est:
        hi = list(n)
        for i in est:
            hi[i] = n[i] / MARGIN
        lo = list(n)
        for i in est:
            lo[i] = n[i] * MARGIN
        return {t for t, f in RULES.items() if f(lo if t == "Higher Potassium" else hi, gl)}
    return {t for t, f in RULES.items() if f(n, gl)}


def contradicted(n, gl, tags, est=()):
    """Publisher tags the published numbers break (estimates are not used to question a publisher)."""
    return sorted(t for t in tags if t in RULES and all(n[i] is not None and i not in est for i in NEEDS[t]) and not RULES[t](n, gl))


def agreement(recipes):
    """Share of DaVita/AAKP recipes where a rule and the dietitians' own tag agree (run before apply)."""
    out = {}
    for t in ("CKD non-dialysis", "Dialysis", "Lower Protein", "Diabetes"):
        rows = [(t in r["diet"]) == RULES[t](r["n"], r.get("gl")) for r in recipes
                if r["sourceName"] in ("DaVita", "AAKP") and all(r["n"][i] is not None for i in NEEDS[t])]
        out[t] = round(100 * sum(rows) / len(rows)) if rows else None
    return out


def apply(recipes):
    """Add the derived tags to rec["diet"]; return {"added": {source: {tag: n}}, "conflicts": [[id, source, tags]]}."""
    added, conflicts = {}, []
    for rec in recipes:
        n, gl = rec["n"], rec.get("gl")
        pub = set(rec["diet"])
        new = derive(n, gl, rec.get("e", ())) - pub
        for t in new:
            a = added.setdefault(rec["sourceName"], {})
            a[t] = a.get(t, 0) + 1
        bad = contradicted(n, gl, pub, rec.get("e", ()))
        if bad:
            conflicts.append([rec["id"], rec["sourceName"], bad])
        rec["diet"] = sorted(pub | new)
    return {"added": added, "conflicts": conflicts}
