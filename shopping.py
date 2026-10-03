#!/usr/bin/env python3
"""Shopping data for the app (gallery/shop.js): every ingredient line of every recipe as an amount in a
base unit (g, ml or pieces) and a shared ingredient key, plus each key's name in every language and its
shop section. The app adds these up over a meal plan.

  python3 shopping.py            # called by build_gallery.py; prints a short report

Amounts come from the English line (or the source line when there is no English). Names in other languages
come from the same line of each translation, with numbers and measuring words removed, so a key is shown
the way the recipes in that language name it.
"""
import json
import re
from collections import Counter, defaultdict

FRAC = {"¼": .25, "½": .5, "¾": .75, "⅓": 1 / 3, "⅔": 2 / 3, "⅛": .125, "⅜": .375, "⅝": .625, "⅞": .875, "⅙": 1 / 6, "⅚": 5 / 6}
# measuring words -> (base unit, amount of base unit)
UNIT = {}
for words, base, f in [
    ("tsp tsps teaspoon teaspoons t", "ml", 4.93), ("tbsp tbsps tbs tbl tablespoon tablespoons tbsp. T", "ml", 14.79),
    ("cup cups c", "ml", 236.6), ("fl-oz floz", "ml", 29.57), ("pint pints pt", "ml", 473.2), ("quart quarts qt", "ml", 946.4),
    ("gallon gallons", "ml", 3785), ("ml milliliter milliliters millilitre millilitres", "ml", 1), ("l liter liters litre litres", "ml", 1000),
    ("dl", "ml", 100), ("pinch pinches", "ml", .3), ("dash dashes", "ml", .6),
    ("oz ounce ounces", "g", 28.35), ("lb lbs pound pounds", "g", 453.6), ("g gram grams gr", "g", 1), ("kg kilogram kilograms", "g", 1000),
]:
    for w in words.split():
        UNIT[w] = (base, f)
NUM = r"(?:\d+\s+\d+/\d+|\d+-\d+/\d+|\d+/\d+|\d+(?:\.\d+)?|[¼½¾⅓⅔⅛⅜⅝⅞⅙⅚]|\d+\s*[¼½¾⅓⅔⅛⅜⅝⅞⅙⅚])"
RX_QTY = re.compile(rf"^\s*(?:about|approx\.?|approximately)?\s*({NUM})(?:\s*(?:-|–|to|or)\s*({NUM}))?\s*", re.I)
RX_SIZE = re.compile(rf"\(\s*(?:about\s*)?({NUM})\s*-?\s*(fl\.?\s*oz|oz|ounce|ounces|lb|lbs|pound|pounds|g|grams?|kg|ml|l)\b[^)]*\)", re.I)
PREP = re.compile(r"\b(chopped|finely|roughly|coarsely|thinly|diced|minced|sliced|grated|shredded|crushed|peeled|seeded|deseeded|trimmed|"
                  r"halved|quartered|cubed|cut|melted|softened|beaten|divided|optional|fresh|freshly|large|medium|small|whole|about|"
                  r"approx|packed|heaping|level|rinsed|drained|cooked|uncooked|raw|boneless|skinless|thawed|to taste|for serving|"
                  r"for garnish|plus more|or more|as needed|if desired|additional|half|halves)\b", re.I)
SKIP = re.compile(r"^(spray|water|ice|ice cubes?|cold water|warm water|hot water|boiling water|cooking spray|nonstick cooking spray|non-stick spray)$")
STAPLE = re.compile(r"\b(salt|pepper(corns?)?|black pepper|oil|olive oil|vinegar|sugar|honey|flour|baking (powder|soda)|vanilla|cumin|paprika|"
                    r"oregano|thyme|basil|cinnamon|nutmeg|ginger|turmeric|coriander|cardamom|clove|chili powder|cayenne|curry|garam masala|"
                    r"bay lea|rosemary|sage|parsley flakes|dried|ground|powder|seasoning|spice|extract|cornstarch|corn starch|yeast|"
                    r"sweetener|stevia|mustard|soy sauce|hot sauce|worcestershire|ketchup|mayonnaise|syrup|cocoa|sesame seeds|bezar|saffron|loomi|"
                    r"black lime|allspice|fennel seed|caraway|cooking spray|mint leaves dried)\b")
SECTIONS = [
    ("meat", r"\b(chicken|beef|lamb|mutton|veal|goat|camel|turkey|steak|mince|ground meat|fish|salmon|tuna|cod|tilapia|sea bass|haddock|"
             r"halibut|shrimp|prawn|crab|scallop|sardine|anchov|trout|mackerel|hamour|grouper|kingfish|liver|meatball|sausage)\b"),
    ("dairy", r"\b(milk|yogurt|yoghurt|laban|cheese|butter|cream|egg|eggs|ghee|labneh|ricotta|mozzarella|parmesan|feta|cheddar|"
              r"cottage|kefir|whipped topping|half-and-half|creamer)\b"),
    ("frozen", r"\bfrozen\b"),
    ("bakery", r"\b(bread|tortilla|pita|bun|roll|bagel|wrap|naan|baguette|croissant|crackers?|breadcrumbs?|panko|english muffin)\b"),
    ("grains", r"\b(rice|pasta|spaghetti|noodle|macaroni|penne|oats|oatmeal|quinoa|couscous|bulgur|freekeh|barley|cereal|cornmeal|"
               r"semolina|vermicelli|lasagna|orzo|farro|jareesh|grits|flour)\b"),
    ("canned", r"\b(canned|can|broth|stock|tomato paste|tomato sauce|passata|beans|chickpeas|lentils|salsa|pesto|marinara|"
               r"coconut milk|olives|pickles?|capers|jam|jelly|peanut butter|tahini|nut butter)\b"),
    ("produce", r"\b(onion|garlic|tomato|lettuce|spinach|carrot|celery|potato|lemon|lime|orange|apple|banana|berr|strawberr|blueberr|"
                r"raspberr|grape|mango|pineapple|peach|pear|plum|melon|watermelon|cucumber|zucchini|courgette|squash|pumpkin|broccoli|"
                r"cauliflower|cabbage|kale|avocado|mushroom|bell pepper|jalape|chili|chilli|scallion|green onion|leek|shallot|"
                r"cilantro|parsley|mint|dill|basil leaves|fresh basil|ginger root|eggplant|aubergine|okra|corn|peas|green beans|"
                r"asparagus|radish|beet|turnip|sweet potato|yam|cassava|arugula|rocket|herbs|fruit|vegetable|dates|figs|pomegranate|"
                r"kiwi|cherr|apricot|coconut|sprouts|bok choy|fennel|artichoke)\b"),
    ("nuts", r"\b(almond|walnut|pecan|cashew|pistachio|peanut|hazelnut|pine nut|seeds|chia|flax|raisin|cranberr|dried fruit|prune)\b"),
]
SECTION_RX = [(k, re.compile(p)) for k, p in SECTIONS]


# common measuring words written out, in case a spelling is too rare to be learned from the recipes
KNOWN = {
    "fr": {"tasse", "tasses", "c à café", "c à soupe", "cuillère à café", "cuillères à café", "cuillère à soupe", "cuillères à soupe",
           "pincée", "pincées", "gramme", "grammes", "litre", "litres", "once", "onces", "livre", "livres"},
    "es": {"taza", "tazas", "cucharada", "cucharadas", "cucharadita", "cucharaditas", "pizca", "onza", "onzas", "libra", "libras", "gramos", "litro", "litros"},
    "id": {"cangkir", "sdm", "sdt", "sendok makan", "sendok teh", "sejumput", "ons", "pon", "gram", "liter"},
    "tl": {"tasa", "kutsara", "kutsarita", "kurot", "onsa", "libra", "gramo", "litro"},
}


def num(t):
    t = t.strip()
    m = re.match(r"^(\d+)\s*([¼½¾⅓⅔⅛⅜⅝⅞⅙⅚])$", t)
    if m:
        return int(m.group(1)) + FRAC[m.group(2)]
    if t in FRAC:
        return FRAC[t]
    m = re.match(r"^(\d+)[\s-]+(\d+)/(\d+)$", t)
    if m:
        return int(m.group(1)) + int(m.group(2)) / int(m.group(3))
    m = re.match(r"^(\d+)/(\d+)$", t)
    if m:
        return int(m.group(1)) / int(m.group(2)) if int(m.group(2)) else None
    try:
        return float(t)
    except ValueError:
        return None


def singular(w):
    if re.search(r"(ss|us|is)$", w):
        return w
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("oes"):
        return w[:-2]
    if re.search(r"(ches|shes|xes)$", w):
        return w[:-2]
    if w.endswith("s") and len(w) > 3:
        return w[:-1]
    return w


def key_of(name):
    n = name.lower().replace("&", " and ")
    n = re.sub(r"\([^)]*\)", " ", n)
    parts = [x for x in n.split(",") if PREP.sub(" ", x).strip()]
    n = parts[0] if parts else ""
    n = re.sub(r"\b(cut|sliced|chopped|diced|torn|broken)\s+(into|in)\b.*$", " ", n)
    n = re.sub(r"^\s*(cans?|jars?|packages?|pkgs?|packets?|bags?|boxes|box|cartons?|bottles?|containers?|tubs?|envelopes?)\b", " ", n)
    n = re.sub(r"\bcloves?\s+(of\s+)?garlic\b|\bgarlic\s+cloves?\b", "garlic clove", n)
    n = re.sub(r"\b(kosher|sea|table|fine|coarse|iodized)\s+salt\b", "salt", n)
    n = re.sub(r"\b(ground|freshly ground|cracked)\s+black\s+pepper\b", "black pepper", n)
    n = re.sub(r"\b(or|plus)\b.*$", " ", n)
    n = PREP.sub(" ", n)
    n = re.sub(r"\b(of|a|an|the|to|and|for|into|in|pieces?|inch|cm|mm|\d+%?)\b", " ", n)
    n = re.sub(r"[^a-z' -]", " ", n)
    words = n.split()
    if not words:
        return ""
    words[-1] = singular(words[-1])
    return " ".join(words)[:48].strip(" -")


def parse(line):
    """(amount, base unit 'g'/'ml'/'pc'/None, key) of one English ingredient line."""
    text = re.sub(r"\s+", " ", (line or "").replace("½", "½")).strip()
    if not text or text.endswith(":"):
        return None
    low = text.lower()
    if re.match(r"^(salt|kosher salt|sea salt) (and|&) (black )?pepper", low):
        return (None, None, "salt and pepper")
    amt, unit = None, None
    m = RX_QTY.match(text)
    rest = text
    if m:
        a, b = num(m.group(1)), num(m.group(2)) if m.group(2) else None
        amt = max(x for x in (a, b) if x is not None) if a is not None else None
        rest = text[m.end():]
    if re.match(r"^half\b", low):
        amt, rest = .5, text[4:]
    # per-item size right after the number: "1 (15-ounce) can beans"
    size = None
    ms = RX_SIZE.match(rest.strip())
    if ms:
        size = ms
        rest = rest.strip()[ms.end():]
    tok = re.match(r"^\s*(fl\.?\s*oz|[A-Za-z]+\.?)\b\.?\s*", rest)
    if tok:
        w = tok.group(1).replace(".", "").replace(" ", "-")
        w = "fl-oz" if w.lower().startswith("fl") else w
        if w in UNIT or (w.lower() in UNIT and w not in ("T", "t")):
            unit, f = UNIT.get(w) or UNIT[w.lower()]
            amt = (amt if amt is not None else 1) * f
            rest = rest[tok.end():]
    name = re.sub(r"^\s*(small|medium|large)?\s*(of\s+)?", "", rest)
    # a weight given for the whole line: "2 medium onions (220 g)", or each: "(about 4 oz each)"
    later = RX_SIZE.search(rest)
    sz = size or later
    if sz and (unit is None or unit == "pc"):
        v, u = num(sz.group(1)), sz.group(2).lower().replace(" ", "").replace(".", "")
        u = "fl-oz" if u.startswith("fl") else u
        if v is not None and u in UNIT:
            per = v * UNIT[u][1]
            each = size is not None or "each" in sz.group(0).lower()
            amt = per * (amt or 1) if each else per
            unit = UNIT[u][0]
    if unit is None and amt is not None:
        unit = "pc"
    k = key_of(name)
    if not k or SKIP.match(k):
        return None
    return (round(amt, 2) if amt is not None else None, unit, k)


def section(k):
    if re.search(r"\b(bell pepper|chili pepper|jalape)", k):
        return "produce"
    if STAPLE.search(k) and not re.search(r"\b(fresh|leaves|root)\b", k):
        return "staples"
    for s, rx in SECTION_RX:
        if rx.search(k):
            return s
    return "other"


def strip_local(line, phrases):
    t = re.sub(r"\([^)]*\)", " ", line or "")
    t = re.split(r"[,،]", t)[0]
    w = re.sub(r"[\d¼½¾⅓⅔⅛⅜⅝⅞⅙⅚.,/\-–—%]+", " ", t).split()
    low = " ".join(w).lower()
    for p in phrases:   # longest first
        if low == p or low.startswith(p + " "):
            w = w[len(p.split()):]
            break
    while w and w[0].lower() in ("de", "d'", "du", "des", "of", "ng", "del"):
        w = w[1:]
    if w and re.match(r"^d['’]", w[0], re.I):
        w[0] = w[0][2:]
    return " ".join(w).strip(" :-")[:60]


def build(recipes, langs):
    """recipes: the app records (with r['t'][lang]['ing']). Returns the shop.js payload and a report."""
    parsed = {}
    for r in recipes:
        base = r["t"].get("en") or r["t"].get(r["src"]) or next(iter(r["t"].values()))
        parsed[r["id"]] = [parse(line) for _, line in base.get("ing", [])]
    # measuring phrases of each language ("ملعقة صغيرة", "cuillère à café de"): leading phrases that follow the number
    # in a good share of the lines for one English unit, and that rarely start a line without a unit
    unit_words = {}
    clean = lambda t: re.sub(r"[\d¼½¾⅓⅔⅛⅜⅝⅞⅙⅚.,/\-–—()%]+", " ", re.split(r"[,،(]", t or "")[0]).lower().split()
    for l in langs:
        by_unit, plain, n_unit, nxt = defaultdict(Counter), Counter(), Counter(), defaultdict(set)
        for r in recipes:
            loc, en = r["t"].get(l), r["t"].get("en")
            if not loc or not en or len(loc.get("ing", [])) != len(en.get("ing", [])):
                continue
            for (_, el), (_, ll) in zip(en["ing"], loc["ing"]):
                m = RX_QTY.match(el or "")
                tok = re.match(r"^\s*([A-Za-z]+)", el[m.end():]) if m else None
                u = tok.group(1).lower() if tok and tok.group(1).lower() in UNIT else None
                w = clean(ll)
                pre = {" ".join(w[:k]) for k in range(1, min(4, len(w)) + 1)}
                if u:
                    n_unit[u] += 1
                    for k in range(1, min(4, len(w)) + 1):
                        x = " ".join(w[:k])
                        by_unit[u][x] += 1
                        nxt[x].add(w[k] if k < len(w) else "")
                else:
                    for x in pre:
                        plain[x] += 1
        phrases = set()
        for u, c in by_unit.items():
            for x, k in c.items():
                # a measuring phrase is followed by many different ingredients ("spoon + salt" is not)
                if n_unit[u] >= 20 and k >= .04 * n_unit[u] and plain[x] <= .15 * k and len(nxt[x]) >= max(25, .03 * k):
                    phrases.add(x)
        phrases |= KNOWN.get(l, set())
        unit_words[l] = sorted(phrases, key=lambda x: -len(x.split()))
    keys, names = {}, defaultdict(lambda: defaultdict(Counter))
    rows = {}
    for r in recipes:
        out = []
        for i, p in enumerate(parsed[r["id"]]):
            if not p:
                continue
            amt, unit, k = p
            if k not in keys:
                keys[k] = len(keys)
            names[k]["en"][k] += 1
            for l in langs:
                loc = r["t"].get(l)
                if loc and len(loc.get("ing", [])) == len(parsed[r["id"]]):
                    nm = strip_local(loc["ing"][i][1], unit_words[l])
                    if len(nm) >= 2:
                        names[k][l][nm] += 1
            out.append([keys[k], amt, {"g": 0, "ml": 1, "pc": 2}.get(unit, 3)])
        rows[r["id"]] = out
    klist = sorted(keys, key=keys.get)
    payload = {
        "keys": [{"s": section(k), "n": {l: (names[k][l].most_common(1)[0][0] if names[k][l] else k) for l in ["en", *langs]}} for k in klist],
        "r": rows,
    }
    total = sum(len(p) for p in parsed.values())
    ok = sum(1 for p in parsed.values() for x in p if x and x[1])
    report = {"lines": total, "with_amount": ok, "keys": len(klist), "sections": Counter(k["s"] for k in payload["keys"]).most_common()}
    return payload, report


if __name__ == "__main__":
    for t in ["1 (15-ounce) can black beans, rinsed", "2 medium onions (220 g)", "4 whole boneless, skinless chicken breasts (about 4 oz each)",
              "1/2 tsp Kosher Salt (divided)", "1-1/2 cups low-sodium chicken broth", "salt & pepper to taste", "120g rocket", "half tsp ground nutmeg",
              "1.5 lb eggplant cut into half inch pieces", "2 cloves garlic, minced", "¼ cup unsweetened cashew milk", "3 teabags (or loose leaf tea)"]:
        print(t, "->", parse(t))
