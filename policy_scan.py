#!/usr/bin/env python3
"""Find text that still mentions excluded ingredients (pork, pork-derived gelatin, alcohol) in any
language and field of the recipes shown in the app.

  python3 policy_scan.py            # report counts
  python3 policy_scan.py --export   # write translations/policy_text_review_v2.json for rewriting

Ingredient lines that match mean the whole recipe must go (ingredient_filter.py); descriptions,
titles, steps and hints that only mention them (as a swap or serving idea) are rewritten through
translations/policy_text_fixes_v2.json and `i18n.py fixes`.
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE / "davita_recipes.db"
# per language; kept specific to avoid false hits (e.g. vinegar, root beer, turkey bacon, grape "anggur")
L = r"A-Za-zÀ-ɏ؀-ۿݐ-ݿऀ-ॿঀ-৿"   # letters and marks of the scripts used


def words(*ws):
    """Whole-word alternatives (works for Arabic, Devanagari and Bengali too, where \\b is unreliable)."""
    return "|".join(rf"(?<![{L}]){w}(?![{L}])" for w in ws)


PAT = {
    "en": words("pork", "bacon", "hams?", "lard", "prosciutto", "pancetta", "pepperoni", "salami", "gelatine?", "jell-?o", "marshmallows?",
                "wines?", "beers?", "rum", "brandy", "vodka", "whiske?y", "bourbon", "sake", "mirin", "liqueurs?", "sherry", "champagne", "cognac", "tequila"),
    "es": words("cerdo", "puerco", "tocino", "jam[oó]n", "manteca de cerdo", "chicharr[oó]n(es)?", "chorizo", "vinos?", "cervezas?", "ron", "brandy",
                "vodka", "gelatina", "licor(es)?", "jerez"),
    "ar": words("خنزير", "الخنزير", "لحم مقدد", "اللحم المقدد", "بيكون", "البيكون", "نبيذ", "النبيذ", "بيرة", "البيرة", "جعة", "كحول", "الكحول",
                "كحولي", "كحولية", "خمر", "الخمر", "جيلاتين", "الجيلاتين", "شمبانيا", "شامبين", "فودكا", "مارشميلو", "المارشميلو"),
    "ur": words("سور", "سؤر", "پورک", "بیکن", "وائن", "بیئر", "شراب", "جیلاٹن", "جلیٹن", "الکحل", "ہیم", "مارش میلو"),
    "hi": words("सूअर", "पोर्क", "बेकन", "वाइन", "बीयर", "शराब", "जिलेटिन", "हैम", "रम", "ब्रांडी", "वोदका", "मार्शमैलो"),
    "fr": words("porc", "lardons?", "bacon", "jambon", "vins?", "bi[eè]res?", "rhum", "g[ée]latine", "saucissons?", "cognac", "liqueurs?", "chamallows?", "guimauves?"),
    "id": words("babi", "bacon", "ham", "wine", "bir", "anggur merah", "anggur putih", "rum", "gelatin", "sake", "mirin", "minuman keras", "alkohol", "marshmallow"),
    "bn": words("শূকর", "শুয়োর", "শুকর", "বেকন", "ওয়াইন", "বিয়ার", "জেলাটিন", "মদ", "অ্যালকোহল", "হ্যাম", "মার্শম্যালো"),
    "tl": words("baboy", "bacon", "ham", "wine", "beer", "alak", "serbesa", "rum", "gelatin", "liempo", "lechon", "marshmallow"),
}
RX = {k: re.compile(v, re.I) for k, v in PAT.items()}
# allowed phrases that look like matches
OK = re.compile(r"turkey bacon|turkey ham|beef bacon|chicken ham|bacon de pavo|tocino de pavo|jam[oó]n de pavo|بيكون الديك الرومي|لحم ديك رومي مقدد|vinegar|vinagre|vinaigre|\bخل\b|سرکہ|सिरका|ভিনেগার|cuka|suka|root beer|ginger beer|non-?alcoholic|sin alcohol|sans alcool|بدون كحول|halal|حلال|rum extract|extracto de ron|gelatin-free|sin gelatina|بدون جيلاتين|agar|marshmallow cr[eè]me", re.I)


def reviewed_keep():
    """Texts already judged fine in translations/policy_v2/out_*.json (kept while the text is unchanged)."""
    keep = set()
    for f in sorted((HERE / "translations" / "policy_v2").glob("out_*.json")):
        for it in json.loads(f.read_text(encoding="utf-8")):
            for lang, t in (it.get("orig") or {}).items():
                if it["action"] == "keep" or (it["action"] == "rewrite" and lang not in it.get("text", {})):
                    keep.add((it["recipe_id"], it["field"], it["position"], t))
            if it["action"] == "keep":
                for t in (it.get("text") or {}).values():
                    keep.add((it["recipe_id"], it["field"], it["position"], t))
    return keep


def hits():
    db = sqlite3.connect(DB)
    shown = {r[0] for r in db.execute("SELECT id FROM recipes WHERE canonical_id = id")}
    out = []
    for lang, rx in RX.items():
        for rid, title, desc in db.execute("SELECT recipe_id, title, description FROM recipe_i18n WHERE lang = ?", (lang,)):
            if rid not in shown:
                continue
            for field, text in (("title", title), ("description", desc)):
                if text and rx.search(text) and not OK.search(rx.search(text).group(0) + " " + text[max(0, rx.search(text).start() - 15): rx.search(text).end() + 15]):
                    out.append({"recipe_id": rid, "lang": lang, "field": field, "position": 0, "text": text})
        for table, field in (("ingredients_i18n", "ingredients"), ("steps_i18n", "steps"), ("hints_i18n", "hints")):
            for rid, pos, text in db.execute(f"SELECT recipe_id, position, text FROM {table} WHERE lang = ?", (lang,)):
                if rid not in shown or not text:
                    continue
                m = rx.search(text)
                if m and not OK.search(text[max(0, m.start() - 15): m.end() + 15]):
                    out.append({"recipe_id": rid, "lang": lang, "field": field, "position": pos, "text": text})
    keep = reviewed_keep()
    # plus the review inputs themselves: an item whose decision was "keep" is listed there with its text
    for f in sorted((HERE / "translations" / "policy_v2").glob("in_*.json")):
        outs = {}
        of = f.with_name(f.name.replace("in_", "out_"))
        if of.exists():
            outs = {o["key"]: o for o in json.loads(of.read_text(encoding="utf-8"))}
        for it in json.loads(f.read_text(encoding="utf-8")):
            if outs.get(it["key"], {}).get("action") == "keep":
                for t in it["text"].values():
                    keep.add((it["recipe_id"], it["field"], it["position"], t))
    return [x for x in out if (x["recipe_id"], x["field"], x["position"], x["text"]) not in keep]


def main():
    h = hits()
    from collections import Counter
    print(len(h), "texts mention excluded items")
    print(Counter((x["field"], x["lang"]) for x in h).most_common())
    if "--export" in sys.argv:
        # one review entry per (recipe, field, position), with the text of each language that matched
        grouped = {}
        for x in h:
            k = (x["recipe_id"], x["position"], x["field"])
            grouped.setdefault(k, {"recipe_id": x["recipe_id"], "position": x["position"], "field": x["field"], "text": {}})["text"][x["lang"]] = x["text"]
        items = sorted(grouped.values(), key=lambda g: (g["recipe_id"], g["field"], g["position"]))
        (HERE / "translations" / "policy_text_review_v2.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        print("wrote translations/policy_text_review_v2.json:", len(items), "items;",
              "ingredient lines (recipe must be excluded):", sum(1 for g in items if g["field"] == "ingredients"))


if __name__ == "__main__":
    main()
