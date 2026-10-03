import json
def L(title, desc, portions, serving, ings, steps):
    return {"title": title, "description": desc, "portions": portions, "serving_size": serving,
            "ingredients": [[None, x] for x in ings], "steps": [[None, x] for x in steps],
            "hints": [], "food_choices": []}
def rec(id, **langs):
    return {"id": id, "translations": langs}
def dump(n, R):
    p = f"/mnt/c/WSL/davita/translations/out_c2_part{n}.json"
    json.dump(R, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", p, len(R))
