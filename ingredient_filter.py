#!/usr/bin/env python3
"""Ingredient policy: remove recipes containing pork, pork-derived gelatin or alcohol.

Matches are checked against every ingredient line and the recipe title, in
English and Spanish. Removed recipes are recorded in the `excluded_recipes`
table with the reason and the exact ingredient lines that matched, so the
decision can be reviewed.

Usage: python3 ingredient_filter.py            # remove and record
       python3 ingredient_filter.py --dry-run  # only report
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent / "davita_recipes.db"

# (reason, pattern, exceptions) -- an exception match on the same line cancels the hit
RULES = [
    ("pork", r"\bpork\b|\bcerdo\b|\bpuerco\b|\bcochinita\b|\bcarnitas\b", None),
    ("pork", r"\bbacon\b|\btocino\b|\btocineta\b|\bpancetta\b|\bprosciutto\b",
     r"\b(turkey|beef|chicken|veggie|vegetarian|pavo|res|pollo)\s+(bacon|tocino|tocineta)\b|imitation bacon"),
    ("pork", r"\bham\b|\bhams\b|\bham hocks?\b|\bjam[oó]n\b",
     r"\b(turkey|chicken|pavo|pollo)\s+(ham|jam[oó]n)\b"),
    ("pork", r"\blard\b|manteca de cerdo|\bmanteca de puerco\b", None),
    ("pork", r"\bsausages?\b|\bsalchichas?\b|\bchorizo\b|\bandouille\b|\bkielbasa\b|\bbratwurst\b",
     r"\b(turkey|chicken|beef|veggie|vegetarian|plant-based|pavo|pollo|res)\b[\w\s,-]{0,25}\b(sausages?|salchichas?|chorizo)\b"
     r"|\b(sausages?|chorizo)\b[\w\s,-]{0,15}\b(turkey|chicken|beef|pavo|pollo)\b|sausage seasoning|homemade turkey sausage"
     r"|\b(salchichas?|chorizo)\s+de\s+(pavo|pollo|res)\b"),
    ("pork", r"\bpepperoni\b|\bsalami\b|\bbologna\b|\bhot ?dogs?\b|\bfrankfurters?\b|\bwieners?\b|\bchicharr?[oó]n(es)?\b|\bpork rinds?\b",
     r"\b(turkey|chicken|beef|pavo|pollo)\s+(pepperoni|salami|bologna|hot ?dogs?|frankfurters?)\b|hot ?dog (rolls?|buns?)"),
    ("pork", r"\b(baby back|spare) ribs?\b|\brack of ribs\b|\bpork ribs?\b", r"\bbeef\b"),
    ("pork-derived gelatin", r"\bgelatine?\b|\bgelatina\b|\bgrenetina\b|\bjell-?o\b(?![^,]*pudding)", r"\bagar\b|halal|kosher|pudding mix"),
    ("pork-derived gelatin", r"\bmarshmallows\b|\bmarshmallow\b(?!\s*(cr[eè]me|cream|fluff))|\bmalvaviscos?\b", None),
    ("alcohol", r"\bwines?\b|\bvino\b|\bsherry\b|\bjerez\b|\bmirin\b|\bsake\b|\bchampagne\b|\bchampa[ñn]a\b|\bchamp[aá]n\b|\bprosecco\b|\blicor\b|\bcoñac\b|\bbrandi\b",
     r"\bvinegar\b|\bvinagre\b|\bvinaigrette\b|\bvinagreta\b|\bwine-free\b|non-alcoholic|sin alcohol"),
    ("alcohol", r"\bbeers?\b|\bcerveza\b|\bstout\b|\blager\b",
     r"\broot beer\b|\bginger beer\b|non-alcoholic|sin alcohol"),
    ("alcohol", r"\brum\b|\bron\b|\bbrandy\b|\bcognac\b|\bvodka\b|\bwhiske?y\b|\bbourbon\b|\btequila\b|\bliqueur\b|\bkahl[uú]a\b|\bamaretto\b|\bgin\b",
     r"^(?!.*\brum\b(?!\s*extract)).*\brum extract\b|\bginger\b|\bgin\b(?=ger)"),
]
COMPILED = [(reason, re.compile(p, re.I), re.compile(x, re.I) if x else None) for reason, p, x in RULES]


def check(lines):
    hits = []
    for line in lines:
        for reason, rx, ex in COMPILED:
            if rx.search(line) and not (ex and ex.search(line)):
                hits.append((reason, line))
                break
    return hits


def main():
    dry = "--dry-run" in sys.argv
    db = sqlite3.connect(DB)
    db.execute("""CREATE TABLE IF NOT EXISTS excluded_recipes (
        id INTEGER PRIMARY KEY, title TEXT, url TEXT, language TEXT, category TEXT,
        reasons TEXT, matched_lines TEXT)""")
    pe = Path(__file__).resolve().parent / "translations" / "policy_exclude.json"
    reviewed = json.loads(pe.read_text(encoding="utf-8")) if pe.exists() else {}
    flagged = []
    for rid, title, url, lang, cat in db.execute(
            "SELECT id, title, url, language, category_en FROM recipes"):
        ing = [t for (t,) in db.execute("SELECT text FROM ingredients WHERE recipe_id=? ORDER BY position", (rid,))]
        hits = check(ing)
        # titles only count for unambiguous pork words (e.g. "Pork Chop Suey", "Compote for Pork")
        if not hits and re.search(r"\bpork\b|\bcerdo\b|\bcarnitas\b", title, re.I):
            hits = [("pork", f"title: {title}")]
        if hits:
            flagged.append((rid, title, url, lang, cat, sorted({h[0] for h in hits}), [h[1] for h in hits]))
        elif str(rid) in reviewed:   # reviewed by hand (translations/policy_exclude.json), e.g. bacon in a step
            flagged.append((rid, title, url, lang, cat, [reviewed[str(rid)]["reason"]], [reviewed[str(rid)]["line"]]))

    by_reason = {}
    for f in flagged:
        for r in f[5]:
            by_reason[r] = by_reason.get(r, 0) + 1
    print(f"{len(flagged)} recipes flagged: {by_reason}")
    for rid, title, _, lang, cat, reasons, lines in sorted(flagged, key=lambda f: (f[5], f[1])):
        print(f"  [{', '.join(reasons)}] {title} ({lang}, {cat}) <- {' | '.join(lines)}")
    if dry:
        return

    ids = [(f[0],) for f in flagged]
    db.executemany("INSERT OR REPLACE INTO excluded_recipes VALUES (?,?,?,?,?,?,?)",
                   [(f[0], f[1], f[2], f[3], f[4], ", ".join(f[5]), " | ".join(f[6])) for f in flagged])
    tables = ["ingredients", "steps", "hints", "food_choices", "recipe_sections", "recipe_terms"]
    tables += [t for (t,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%_i18n'")]
    for table in tables:
        db.executemany(f"DELETE FROM {table} WHERE recipe_id=?", ids)
    db.executemany("DELETE FROM recipes WHERE id=?", ids)
    db.commit()
    left = db.execute("SELECT count(*) FROM recipes").fetchone()[0]
    print(f"Removed {len(ids)} recipes; {left} remain. Details in table excluded_recipes.")


if __name__ == "__main__":
    main()
