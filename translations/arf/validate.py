#!/usr/bin/env python3
"""Check a feminine-Arabic batch: python3 validate.py <n>"""
import json, sys, re
from pathlib import Path
H = Path(__file__).resolve().parent
n = sys.argv[1]
src = json.loads((H / f"jobs_{n}.json").read_text(encoding="utf-8"))
out = {o["id"]: o for o in json.loads((H / f"out_{n}.json").read_text(encoding="utf-8"))}
err = []
for j in src:
    o = out.get(j["id"])
    if not o: err.append(f"{j['id']} missing"); continue
    for k in ("steps", "hints"):
        if len(o.get(k) or []) != len(j[k]): err.append(f"{j['id']} {k} count {len(o.get(k) or [])} != {len(j[k])}")
        for a, b in zip(j[k], o.get(k) or []):
            if not (isinstance(b, list) and len(b) == 2): err.append(f"{j['id']} {k} bad item"); break
            na, nb = re.findall(r"\d+", a[1] or ""), re.findall(r"\d+", b[1] or "")
            if sorted(na) != sorted(nb): err.append(f"{j['id']} {k} numbers changed: {a[1][:40]}")
print("OK" if not err else "\n".join(err[:30]) + f"\n{len(err)} problems")
