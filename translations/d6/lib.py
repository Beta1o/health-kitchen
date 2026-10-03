import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
JOBS = {j["id"]: j for j in json.loads((ROOT/"jobs_d6.json").read_text(encoding="utf-8"))}
GL = {"es": {"Fruit/veg portions": "Porciones de fruta/verdura", "For the salsa": "Para la salsa", "For the marinade": "Para el adobo", "For the sponge": "Para el bizcocho", "For the custard": "Para la crema pastelera", "For the topping": "Para la cobertura", "For the jelly": "Para la gelatina"},
      "ar": {"Fruit/veg portions": "حصص الفاكهة/الخضار", "For the salsa": "للصلصة", "For the marinade": "للتتبيلة", "For the sponge": "لكعكة الإسفنج", "For the custard": "للكاسترد", "For the topping": "للتغطية", "For the jelly": "للجيلي"}}
FV = {"es": "Porciones de fruta/verdura por ración: {}", "ar": "حصص الفاكهة/الخضار لكل حصة: {}"}
def mk(lang, jid, t):
    j = JOBS[jid]
    title, desc, por, ser, ings, steps, hints, fc = t
    def pair(src, texts):
        assert len(src) == len(texts), (jid, lang, len(src), len(texts))
        res = []
        for (g, s), x in zip(src, texts):
            if x == "@FV":
                x = FV[lang].format(re.search(r"(\d+)\s*$", s).group(1))
            res.append([None if g is None else GL[lang][g], x])
        return res
    assert len(fc) == len(j["food_choices"]), (jid, "fc")
    return {"title": title, "description": desc, "portions": por, "serving_size": ser,
            "ingredients": pair(j["ingredients"], ings), "steps": pair(j["steps"], steps),
            "hints": pair(j["hints"], hints), "food_choices": fc}
def build(n, recs):
    out = [{"id": jid, "translations": {"es": mk("es", jid, es), "ar": mk("ar", jid, ar)}} for jid, es, ar in recs]
    (ROOT/f"out_d6_part{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
