import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
JOBS = {j["id"]: j for j in json.loads((ROOT/"jobs_d3.json").read_text(encoding="utf-8"))}
GL = {"es": {"Fruit/veg portions": "Porciones de fruta/verdura", "For the hot pepper sauce": "Para la salsa picante", "For the burgers": "Para las hamburguesas", "For the sauce": "Para la salsa", "Sauce": "Salsa", "Chargrilled veggies": "Verduras a la parrilla", "For the marinade": "Para el adobo", "For the rice": "Para el arroz", "Salad": "Ensalada", "For the dressing": "Para el aderezo", "For the salsa": "Para la salsa", "For the garnish": "Para decorar"},
      "ar": {"Fruit/veg portions": "حصص الفاكهة/الخضار", "For the hot pepper sauce": "لصلصة الفلفل الحار", "For the burgers": "للبرغر", "For the sauce": "للصلصة", "Sauce": "الصلصة", "Chargrilled veggies": "خضار مشوية على الفحم", "For the marinade": "للتتبيلة", "For the rice": "للأرز", "Salad": "السلطة", "For the dressing": "للتتبيلة", "For the salsa": "للسالسا", "For the garnish": "للتزيين"}}
GL["ar"]["For the marinade"] = "للمخلل (التتبيلة)"
GL["ar"]["For the marinade"] = "للتتبيل"
GL["ar"]["For the dressing"] = "للصلصة"
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
    (ROOT/f"out_d3_part{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
