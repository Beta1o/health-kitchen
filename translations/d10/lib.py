import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
JL = json.loads((ROOT/"jobs_d10.json").read_text(encoding="utf-8"))
GL = {"es": {"Fruit/veg portions": "Porciones de fruta/verdura", "For the dressing": "Para el aderezo", "For the salad": "Para la ensalada",
             "For the croutons": "Para los crutones", "For the marinade": "Para el adobo", "For the kebabs": "Para las brochetas"},
      "ar": {"Fruit/veg portions": "حصص الفاكهة/الخضار", "For the dressing": "للتتبيلة", "For the salad": "للسلطة",
             "For the croutons": "للخبز المحمص (الكروتون)", "For the marinade": "للمتبّل", "For the kebabs": "للكباب"}}
FV = {"es": "Porciones de fruta/verdura por ración: {}", "ar": "حصص الفاكهة/الخضار لكل حصة: {}"}
def mk(lang, j, t):
    title, desc, por, ser, ings, steps, hints, fc = t
    if por == "@P": por = j["portions"]
    if ser == "@S":
        n = re.match(r"(\d+)", j["serving_size"]).group(1)
        ser = f"{n} g" if lang == "es" else f"{n} غرام"
    def pair(src, texts):
        assert len(src) == len(texts), (j["id"], lang, len(src), len(texts))
        res = []
        for (g, s), x in zip(src, texts):
            if x == "@FV":
                x = FV[lang].format(re.search(r"(\d+)\s*$", s).group(1))
            res.append([None if g is None else GL[lang][g], x])
        return res
    assert len(fc) == len(j["food_choices"])
    return {"title": title, "description": desc, "portions": por, "serving_size": ser,
            "ingredients": pair(j["ingredients"], ings), "steps": pair(j["steps"], steps),
            "hints": pair(j["hints"], hints), "food_choices": fc}
def build(n, recs):
    out = []
    for idx, es, ar in recs:
        j = JL[idx]
        out.append({"id": j["id"], "translations": {"es": mk("es", j, es), "ar": mk("ar", j, ar)}})
    (ROOT/f"out_d10_part{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
