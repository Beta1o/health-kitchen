#!/usr/bin/env python3
"""Combine the healthy Saudi batches (out/s*.json) into recipes.json and add diet tags.

Diet tags come from the computed nutrition per serving (USDA SR Legacy, see nutrition/usda.py)
and from the ingredients, with fixed thresholds so every recipe is judged the same way:
  Diabetes          carbohydrates <= 60 g and added sugar <= 6 g
  Heart Healthy     sodium <= 600 mg, fat <= 20 g, cholesterol <= 100 mg
  CKD non-dialysis  sodium <= 600 mg, potassium <= 500 mg, phosphorus <= 250 mg, protein <= 25 g
  Dialysis          sodium <= 600 mg, potassium <= 500 mg, phosphorus <= 300 mg
  Lower Potassium   potassium <= 250 mg
  Vegetarian        no meat, poultry or fish in the ingredients
  Gluten-free       no wheat, barley, bulgur, freekeh, semolina, oats or bread products
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEAT = re.compile(r"\b(lamb|mutton|beef|veal|goat|camel|chicken|turkey|pigeon|meat|liver|trotters|fish|shrimp|prawn|tuna|salmon|grouper|kingfish|anchov|sardine)\w*", re.I)
GLUTEN = re.compile(r"\b(wheat|flour|bread|bulgur|burghul|freekeh|farik|barley|semolina|oats?|oatmeal|vermicelli|pasta|couscous|jareesh|jarish|crushed wheat|filo|phyllo|puff pastry|biscuit|samboosa|kunafa|dough)\w*", re.I)


def diets(r, en_ingredients):
    n = r["nutrients"]
    out = []
    if n["carbohydrates_g"] <= 60 and n["added_sugar_g"] <= 6:
        out.append("Diabetes")
    if n["sodium_mg"] <= 600 and n["fat_g"] <= 20 and n["cholesterol_mg"] <= 100:
        out.append("Heart Healthy")
    if n["sodium_mg"] <= 600 and n["potassium_mg"] <= 500 and n["phosphorus_mg"] <= 250 and n["protein_g"] <= 25:
        out.append("CKD non-dialysis")
    if n["sodium_mg"] <= 600 and n["potassium_mg"] <= 500 and n["phosphorus_mg"] <= 300:
        out.append("Dialysis")
    if n["potassium_mg"] <= 250:
        out.append("Lower Potassium")
    text = " ".join(line for _, line in en_ingredients)
    if not MEAT.search(text):
        out.append("Vegetarian")
    if not GLUTEN.search(text):
        out.append("Gluten-free")
    return out


SUIT = {"Diabetes": ("people with diabetes", "مرضى السكري"), "Heart Healthy": ("heart health and blood pressure", "صحة القلب وضغط الدم"),
        "CKD non-dialysis": ("kidney disease (not on dialysis)", "مرضى الكلى غير المحتاجين للغسيل"), "Dialysis": ("people on dialysis", "مرضى غسيل الكلى"),
        "Vegetarian": ("vegetarians", "النباتيين"), "Gluten-free": ("a gluten-free diet", "نظام خالٍ من الغلوتين")}


def suitable(diet, lang):
    names = [SUIT[d][0 if lang == "en" else 1] for d in diet if d in SUIT]
    if not names:
        return ("Best kept as an occasional dish for kidney, diabetes and heart diets; keep to one serving." if lang == "en"
                else "يُفضّل تناوله باعتدال وفي مناسبات لمرضى الكلى والسكري والقلب، مع الالتزام بحصة واحدة.")
    return ("Suitable for: " + ", ".join(names) + "." if lang == "en" else "مناسبة لـ: " + "، ".join(names) + ".")


def main():
    recs = []
    for f in sorted((HERE / "out").glob("s*.json"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0)):
        recs += json.loads(f.read_text(encoding="utf-8"))
    by = {r["source_id"]: r for r in recs}
    for r in recs:
        en = r if r["lang"] == "en" else by.get(r["source_id"] + "-en")
        r["diet"] = diets(r, (en or r)["ingredients"])
        r["cuisine"] = ["Saudi"]
        r["source_name"] = "Saudi Kitchen"
        # plain dish names (the whole collection is made healthier, so no "Healthy" in titles)
        r["title"] = re.sub(r"^\s*Healthy\s+|\s+صحي[ةه]?$|\s*ال?صحي[ةه]?(?=\s|$)", " ", r["title"]).strip()
        # no "Saudi" either: every dish here is already in the Saudi cuisine
        if r["source_id"].startswith("saudi-coffee"):
            r["title"] = "القهوة العربية" if r["lang"] == "ar" else "Arabic Coffee"
        r["title"] = re.sub(r"^\s*Saudi[- ]style\s+|^\s*Saudi\s+|\s+\(?Saudi[- ]style\)?|\s*ال?سعودي[ةه]?(?=\s|$)", " ", r["title"])
        r["title"] = re.sub(r"\s{2,}", " ", r["title"]).strip()
        # who the dish suits, from the same diet tags (last hint before the references)
        line = suitable(r["diet"], r["lang"])
        if line and not any(h[1].startswith(("Suitable for", "مناسبة لـ", "Best kept as")) for h in r["hints"]):
            refs = [h for h in r["hints"] if h[1].startswith(("References", "المراجع", "مراجع"))]
            rest = [h for h in r["hints"] if h not in refs]
            r["hints"] = rest + [[None, line]] + refs
    (HERE / "recipes.json").write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")
    dishes = len([r for r in recs if r["lang"] == "ar"])
    (HERE / "report.json").write_text(json.dumps({"listed": len(json.loads((HERE / "dishes.json").read_text(encoding="utf-8"))),
        "scraped": dishes, "with_image": 0, "with_nutrients": dishes, "skipped": 0,
        "notes": "Healthy home versions written from the encyclopediacooking.com Saudi listing, each checked against at least two other sources; nutrition from USDA SR Legacy."}, indent=1))
    print(f"{dishes} dishes, {len(recs)} records")


if __name__ == "__main__":
    main()
