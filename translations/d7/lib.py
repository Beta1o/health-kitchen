import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
JOBS = {j["id"]: j for j in json.loads((ROOT/"jobs_d7.json").read_text(encoding="utf-8"))}
GL = {"es": {"Fruit/veg portions": "Porciones de fruta/verdura", "For the filling": "Para el relleno", "For the chana chaat": "Para el chana chaat", "For the dressing": "Para el aderezo", "For the mint chutney": "Para el chutney de menta", "For the dough": "Para la masa", "Toppings": "Para acompañar"},
      "ar": {"Fruit/veg portions": "حصص الفاكهة/الخضار", "For the filling": "للحشوة", "For the chana chaat": "للحمص الهندي (تشانا تشات)", "For the dressing": "للتتبيلة", "For the mint chutney": "لصلصة النعناع (تشاتني)", "For the dough": "للعجينة", "Toppings": "للتزيين"}}
FV = re.compile(r"Fruit/veg portions per serving: (\d+)")
FVT = {"es": "Porciones de fruta/verdura por ración: {}", "ar": "حصص الفاكهة/الخضار لكل حصة: {}"}
G = {"es": "g", "ar": "غرام"}
def mk(lang, jid, t):
    j = JOBS[jid]
    title, desc, ings, steps, hints = t
    ser = re.sub(r"(\d+)g$", lambda m: f"{m.group(1)} {G[lang]}", j["serving_size"])
    def pair(src, texts, name):
        assert len(src) == len(texts), (jid, lang, name, len(src), len(texts))
        return [[None if g is None else GL[lang][g], x] for (g, _), x in zip(src, texts)]
    hs = list(hints); full = []
    for _, x in j["hints"]:
        m = FV.fullmatch(x)
        full.append(FVT[lang].format(m.group(1)) if m else hs.pop(0))
    assert not hs, (jid, lang, "hints extra")
    return {"title": title, "description": desc, "portions": j["portions"], "serving_size": ser,
            "ingredients": pair(j["ingredients"], ings, "ing"), "steps": pair(j["steps"], steps, "steps"),
            "hints": pair(j["hints"], full, "hints"), "food_choices": []}
def build(n, recs):
    out = [{"id": jid, "translations": {"es": mk("es", jid, es), "ar": mk("ar", jid, ar)}} for jid, es, ar in recs]
    (ROOT/f"out_d7_part{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
