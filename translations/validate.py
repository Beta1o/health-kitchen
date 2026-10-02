#!/usr/bin/env python3
"""Check a translation batch against its jobs file: python3 validate.py <batch number>"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
n = sys.argv[1]
jobs = json.loads((HERE / f"jobs_{n}.json").read_text(encoding="utf-8"))
try:
    out = json.loads((HERE / f"out_{n}.json").read_text(encoding="utf-8"))
except Exception as e:  # noqa: BLE001
    sys.exit(f"cannot read out_{n}.json: {e}")

ARABIC = re.compile(r"[؀-ۿ]")
SPANISH_HINT = re.compile(r"[áéíóúñ¿¡]|\b(de|la|el|con|y|taza|cucharad\w*)\b", re.I)
KEYS = ("title", "description", "portions", "serving_size", "ingredients", "steps", "hints", "food_choices")
errors = []
by_id = {o.get("id"): o for o in out}
if len(out) != len(jobs):
    errors.append(f"recipe count {len(out)} != {len(jobs)}")
for j in jobs:
    o = by_id.get(j["id"])
    if not o:
        errors.append(f"{j['id']} missing"); continue
    tr = o.get("translations") or {}
    for lang in j["translate_to"]:
        d = tr.get(lang)
        if not isinstance(d, dict):
            errors.append(f"{j['id']} {lang} missing"); continue
        for k in KEYS:
            if k not in d:
                errors.append(f"{j['id']} {lang} lacks key {k}")
        for k in ("ingredients", "steps", "hints", "food_choices"):
            if len(d.get(k) or []) != len(j[k] or []):
                errors.append(f"{j['id']} {lang} {k}: {len(d.get(k) or [])} items, expected {len(j[k] or [])}")
        for k in ("ingredients", "steps", "hints"):
            if any(not (isinstance(p, list) and len(p) == 2) for p in d.get(k) or []):
                errors.append(f"{j['id']} {lang} {k}: items must be [group, text] pairs")
        for k in ("description", "portions", "serving_size"):
            if (j.get(k) is None) != (d.get(k) is None):
                errors.append(f"{j['id']} {lang} {k}: null mismatch")
        texts = [d.get("title") or ""] + [p[1] for k in ("ingredients", "steps") for p in d.get(k) or []
                                          if isinstance(p, list) and len(p) == 2 and p[1]]
        if lang == "ar":
            bad = [t for t in texts if not ARABIC.search(t) and re.search(r"[A-Za-z]{4,}", t)]
            if bad:
                errors.append(f"{j['id']} ar possibly untranslated: {bad[:2]}")
        elif lang == "es" and j["source_lang"] == "en":
            if not any(SPANISH_HINT.search(t) for t in texts[1:]) and len(texts) > 2:
                errors.append(f"{j['id']} es looks untranslated")
print("OK" if not errors else "\n".join(errors[:40]) + f"\n{len(errors)} problems")
