import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from crosscheck import nums
HERE = Path(__file__).resolve().parent.parent
n = int(sys.argv[1]); size = 10
jobs = json.loads((HERE / "jobs_b3.json").read_text(encoding="utf-8"))[(n-1)*size:n*size]
out = json.loads((HERE / f"out_b3_part{n}.json").read_text(encoding="utf-8"))
assert [o["id"] for o in out] == [j["id"] for j in jobs], "id order mismatch"
for j, o in zip(jobs, out):
    for lang in j["translate_to"]:
        d = o["translations"][lang]
        for k in ("ingredients", "steps", "hints", "food_choices"):
            if len(d[k]) != len(j[k]): print(j["id"], lang, k, "count", len(d[k]), len(j[k]))
        for k in ("ingredients", "steps", "hints"):
            for a, b in zip(j[k], d[k]):
                if (a[0] is None) != (b[0] is None): print(j["id"], lang, k, "group null mismatch")
        for k in ("description", "portions", "serving_size"):
            if (j[k] is None) != (d[k] is None): print(j["id"], lang, k, "null mismatch")
        pairs = [(j["title"], d["title"])] + [(a[1], b[1]) for k in ("ingredients","steps","hints") for a, b in zip(j[k], d[k])] + list(zip(j["food_choices"], d["food_choices"]))
        for a, b in pairs:
            m = nums(a) - nums(b)
            if m: print(j["id"], lang, dict(m), a[:60], "||", b[:60])
        for k in ("hints",):
            for a, b in zip(j[k], d[k]):
                if a[1].count("\n\n") != b[1].count("\n\n"): print(j["id"], lang, "paragraph count differs")
                if len(b[1]) < 0.7*len(a[1]): print(j["id"], lang, "hint suspiciously short", len(b[1]), len(a[1]))
print("checked part", n)
