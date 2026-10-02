import json
N = None
def rec(id, es, ar):
    return {"id": id, "translations": {"es": fix(es), "ar": fix(ar)}}
def fix(d):
    for k in ("ingredients", "steps", "hints"):
        d[k] = [list(p) if isinstance(p, (list, tuple)) else [None, p] for p in d[k]]
    return d
def dump(n, R):
    p = f"/mnt/c/WSL/davita/translations/out_b4_part{n}.json"
    json.dump(R, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", p, len(R))
