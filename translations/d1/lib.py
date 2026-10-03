import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
JOBS = {j["id"]: j for j in json.loads((ROOT/"jobs_d1.json").read_text(encoding="utf-8"))}
GL = {"es": {"Fruit/veg portions": "Porciones de fruta/verdura", "For the dip": "Para la salsa", "For the pastry": "Para la masa", "For the filling": "Para el relleno", "For the courgetti spaghetti": "Para los espaguetis de calabacita", "For the watercress sauce": "Para la salsa de berro", "For the drizzle": "Para el glaseado", "For the salad": "Para la ensalada", "For the dressing": "Para el aderezo"},
      "ar": {"Fruit/veg portions": "حصص الفاكهة/الخضار", "For the dip": "للصلصة", "For the pastry": "للعجينة", "For the filling": "للحشوة", "For the courgetti spaghetti": "لسباغيتي الكوسا", "For the watercress sauce": "لصلصة الجرجير", "For the drizzle": "للشراب", "For the salad": "للسلطة", "For the dressing": "للتتبيلة"}}
def mk(lang, jid, t):
    j = JOBS[jid]
    title, desc, por, ser, ings, steps, hints, fc = t
    def pair(src, texts):
        assert len(src) == len(texts), (jid, lang, len(src), len(texts))
        out = []
        for (g, _), x in zip(src, texts):
            if g is not None and g not in GL[lang]: raise KeyError((jid, g))
            out.append([None if g is None else GL[lang][g], x])
        return out
    assert len(fc) == len(j["food_choices"]), (jid, "fc")
    return {"title": title, "description": desc, "portions": por, "serving_size": ser,
            "ingredients": pair(j["ingredients"], ings), "steps": pair(j["steps"], steps),
            "hints": pair(j["hints"], hints), "food_choices": fc}
def build(n, recs):
    out = []
    for jid, es, ar in recs:
        out.append({"id": jid, "translations": {"es": mk("es", jid, es), "ar": mk("ar", jid, ar)}})
    (ROOT/f"out_d1_part{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
