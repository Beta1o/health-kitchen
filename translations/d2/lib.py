import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
JOBS = {j["id"]: j for j in json.loads((ROOT/"jobs_d2.json").read_text(encoding="utf-8"))}
GL = {"es": {"Fruit/veg portions": "Porciones de fruta/verdura", "For the dumplings": "Para las bolitas de masa", "Cold fillings": "Rellenos fríos", "For the pilau rice": "Para el arroz pilaf", "For the topping": "Para la cobertura", "For the chocolate sauce": "Para la salsa de chocolate", "Warm fillings": "Rellenos calientes", "To serve": "Para servir"},
      "ar": {"Fruit/veg portions": "حصص الفاكهة/الخضار", "For the dumplings": "للكرات العجينية", "Cold fillings": "الحشوات الباردة", "For the pilau rice": "لأرز البيلاف", "For the topping": "للتغطية", "For the chocolate sauce": "لصلصة الشوكولاتة", "Warm fillings": "الحشوات الساخنة", "To serve": "للتقديم"}}
def mk(lang, jid, t):
    j = JOBS[jid]
    title, desc, por, ser, ings, steps, hints, fc = t
    def pair(src, texts, name):
        assert len(src) == len(texts), (jid, lang, name, len(src), len(texts))
        out = []
        for (g, _), x in zip(src, texts):
            if g is not None and g not in GL[lang]: raise KeyError((jid, g))
            out.append([None if g is None else GL[lang][g], x])
        return out
    assert len(fc) == len(j["food_choices"]), (jid, "fc")
    return {"title": title, "description": desc, "portions": por, "serving_size": ser,
            "ingredients": pair(j["ingredients"], ings, "ing"), "steps": pair(j["steps"], steps, "steps"),
            "hints": pair(j["hints"], hints, "hints"), "food_choices": fc}
def build(n, recs):
    out = []
    for jid, es, ar in recs:
        out.append({"id": jid, "translations": {"es": mk("es", jid, es), "ar": mk("ar", jid, ar)}})
    (ROOT/f"out_d2_part{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
