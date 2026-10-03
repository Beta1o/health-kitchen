#!/usr/bin/env python3
"""Catch misaligned or altered translations: every number in a source line must
appear in the matching translated line. Usage: python3 crosscheck.py [batch ...]"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path("/mnt/c/WSL/davita/translations")
FRAC = {"½": " 1/2", "⅓": " 1/3", "⅔": " 2/3", "¼": " 1/4", "¾": " 3/4", "⅛": " 1/8", "⅜": " 3/8",
        "⅝": " 5/8", "⅞": " 7/8", "⅕": " 1/5", "⅙": " 1/6"}
AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
# number words some translators use instead of digits
WORDS = {"دقيقتين": "2", "ساعتين": "2", "مرتين": "2", "ملعقتين": "2", "كوبين": "2"}


def nums(s):
    s = (s or "").translate(AR_DIGITS)
    for k, v in FRAC.items():
        s = s.replace(k, v)
    for k, v in WORDS.items():
        s = s.replace(k, f" {v} ")
    return Counter(re.findall(r"\d+(?:\.\d+)?", s))


def check(n):
    jobs = json.loads((HERE / f"jobs_{n}.json").read_text(encoding="utf-8"))
    out = {o["id"]: o for o in json.loads((HERE / f"out_{n}.json").read_text(encoding="utf-8"))}
    bad = []
    for j in jobs:
        for lang, d in out[j["id"]]["translations"].items():
            pairs = [(j["title"], d.get("title"))]
            for k in ("ingredients", "steps", "hints"):
                pairs += [(a[1], b[1]) for a, b in zip(j[k], d.get(k) or [])]
            pairs += list(zip(j["food_choices"], d.get("food_choices") or []))
            for a, b in pairs:
                missing = nums(a) - nums(b)
                if missing:
                    bad.append((j["id"], lang, dict(missing), a[:70], (b or "")[:70]))
    return len(jobs), bad


if __name__ == "__main__":
    batches = sys.argv[1:] or sorted(p.stem.split("_")[1] for p in HERE.glob("out_*.json") if "part" not in p.stem)
    for n in batches:
        total, bad = check(n)
        lines = {(b[0], b[1]) for b in bad}
        print(f"batch {n}: {total} recipes, {len(bad)} lines with missing numbers in {len(lines)} recipe-languages")
        for b in bad[:99]:
            print("   ", b)
