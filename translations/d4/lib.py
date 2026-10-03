import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
JOBS = {j["id"]: j for j in json.loads((ROOT/"jobs_d4.json").read_text(encoding="utf-8"))}
GL = {"es": {"Fruit/veg portions": "Porciones de fruta/verdura", "For the sauce": "Para la salsa", "For the chowder": "Para la sopa cremosa", "For the meatballs": "Para las albóndigas", "For the toppings": "Para decorar", "For the savoury filling": "Para el relleno salado", "For the filling": "Para el relleno", "For the dressing": "Para el aderezo", "To make the eyeballs": "Para hacer los ojos", "For the croutons": "Para los crutones", "For the pastry": "Para la masa", "For the greens": "Para las verduras de hoja"},
      "ar": {"Fruit/veg portions": "حصص الفاكهة/الخضار", "For the sauce": "للصلصة", "For the chowder": "للشوربة الكريمية", "For the meatballs": "لكرات اللحم", "For the toppings": "للتزيين", "For the savoury filling": "للحشوة المالحة", "For the filling": "للحشوة", "For the dressing": "للتتبيلة", "To make the eyeballs": "لصنع العيون", "For the croutons": "للخبز المحمص", "For the pastry": "للعجينة", "For the greens": "للخضار الورقية"}}
def mk(lang, jid, t):
    j = JOBS[jid]
    title, desc, por, ser, ings, steps, hints, fc = t
    def pair(src, texts):
        assert len(src) == len(texts), (jid, lang, len(src), len(texts))
        return [[None if g is None else GL[lang][g], x] for (g, _), x in zip(src, texts)]
    assert len(fc) == len(j["food_choices"]), (jid, "fc")
    return {"title": title, "description": desc, "portions": por, "serving_size": ser,
            "ingredients": pair(j["ingredients"], ings), "steps": pair(j["steps"], steps),
            "hints": pair(j["hints"], hints), "food_choices": fc}
def build(n, recs):
    out = [{"id": jid, "translations": {"es": mk("es", jid, es), "ar": mk("ar", jid, ar)}} for jid, es, ar in recs]
    (ROOT/f"out_d4_part{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
