#!/usr/bin/env python3
"""Build out_b1_partN.json from b1/pN.py data modules. Usage: python3 b1/gen.py N"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
jobs = {j["id"]: j for j in json.loads((ROOT / "jobs_b1.json").read_text(encoding="utf-8"))}
order = [j["id"] for j in json.loads((ROOT / "jobs_b1.json").read_text(encoding="utf-8"))]


def build(src, t):
    g = t.get("groups", {})
    out = {k: t[k] for k in ("title", "description", "portions", "serving_size")}
    for key, short in (("ingredients", "ing"), ("steps", "steps"), ("hints", "hints")):
        items = t[short]
        assert len(items) == len(src[key]), (src["id"], key, len(items), len(src[key]))
        out[key] = [[None if s[0] is None else g[s[0]], txt] for s, txt in zip(src[key], items)]
    assert len(t["fc"]) == len(src["food_choices"]), (src["id"], "fc")
    out["food_choices"] = t["fc"]
    for k in ("description", "portions", "serving_size"):
        assert (src[k] is None) == (out[k] is None), (src["id"], k)
    return out


n = sys.argv[1]
spec = importlib.util.spec_from_file_location(f"p{n}", HERE / f"p{n}.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
res = []
for r in mod.RECIPES:
    src = jobs[r["id"]]
    res.append({"id": r["id"], "translations": {lang: build(src, r[lang]) for lang in src["translate_to"]}})
ids = [r["id"] for r in res]
i0 = order.index(ids[0])
assert ids == order[i0:i0 + len(ids)], "order mismatch"
(ROOT / f"out_b1_part{n}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"part {n}: {len(res)} recipes ({ids[0]}..{ids[-1]})")
