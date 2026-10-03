import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
JOBS = {j["id"]: j for j in json.loads((ROOT/"jobs_d5.json").read_text(encoding="utf-8"))}
GL = {"es": {"Fruit/veg portions": "Porciones de fruta/verdura", "For the batter": "Para la masa líquida", "For the satay sauce": "Para la salsa satay", "For the dressing": "Para el aderezo", "For the relish": "Para el relish", "For the cheesy garlic popcorn topping": "Para el condimento de palomitas con queso y ajo", "For the chilli lemon popcorn topping": "Para el condimento de palomitas con chile y limón", "For the vegetables": "Para las verduras", "For the side salad": "Para la ensalada de acompañamiento", "For the topping": "Para la cobertura", "For the dip": "Para la salsa para mojar", "For the parsnip crisps": "Para las chips de chirivía", "For the sesame yoghurt": "Para el yogur de sésamo"},
      "ar": {"Fruit/veg portions": "حصص الفاكهة/الخضار", "For the batter": "للعجينة السائلة", "For the satay sauce": "لصلصة الساتاي", "For the dressing": "للتتبيلة", "For the relish": "للمخلل الحار", "For the cheesy garlic popcorn topping": "لتتبيلة الفشار بالجبن والثوم", "For the chilli lemon popcorn topping": "لتتبيلة الفشار بالفلفل الحار والليمون", "For the vegetables": "للخضار", "For the side salad": "لسلطة الجانب", "For the topping": "للتغطية", "For the dip": "للغمس", "For the parsnip crisps": "لشرائح الجزر الأبيض المقرمشة", "For the sesame yoghurt": "لزبادي السمسم"}}
def mk(lang, jid, t):
    j = JOBS[jid]
    if len(t) == 7: t = tuple(t) + ([],)
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
    (ROOT/f"out_d5_part{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
