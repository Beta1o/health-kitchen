#!/usr/bin/env python3
"""Dish-type tags and the Vegetarian tag worked out from a recipe's own text and times, with the same rules for
every source. Only tags with objective evidence are derived; Budget, Easy, Potluck, Picnic, Freezer, Refrigerator,
One-Dish Meal and Candy are a publisher's judgement and are not. Publisher tags are kept.

  5 or less ingredients   at most 5 ingredient lines (as DaVita counts: every line)
  Quick                   prep + cook time 30 minutes or less (times that include chilling, marinating, ... are not)
  Soup, Stew, Cake, Muffin, Cookies, Bread, Pie, Stir-fry   the dish named in the title (Bread and Cake also by category)
  Meatless Entree         a vegetarian main dish (main category, at least 250 kcal and 10 g protein a serving)
  Vegetarian              no meat, poultry, fish or seafood, gelatin or meat stock in the ingredients

The build prints how often each rule agrees with the DaVita and ADA tags (publishers tag sparingly, so a rule
finds more recipes than they tagged; agreement is measured as the share of publisher-tagged recipes found).
"""
import re

MAINS = {"Chicken & Turkey", "Beef, Lamb & Pork", "Fish & Seafood", "Pasta, Rice & Grains", "Soups & Stews",
         "Pizza & Sandwiches"}
UNIT_H = re.compile(r"(\d+(?:\.\d+)?)\s*(h|hrs?|hours?|m|mins?|minutes?)\b")
WAIT = re.compile(r"chill|freez|marinat|overnight|refrig|rest|soak|stand|set|rise|prove", re.I)


def minutes(s):
    if not s:
        return None
    s = s.lower().strip()
    if WAIT.search(s):
        return 999
    m = re.fullmatch(r"pt(?:(\d+)h)?(?:(\d+)m)?", s)
    if m:
        return int(m.group(1) or 0) * 60 + int(m.group(2) or 0)
    found = UNIT_H.findall(s)
    if not found:
        return None
    return sum(float(n) * (60 if u.startswith("h") else 1) for n, u in found)


def total_minutes(prep, cook, total):
    t = minutes(total)
    if t is not None:
        return t
    a, b = minutes(prep), minutes(cook)
    return None if a is None and b is None else (a or 0) + (b or 0)


def _t(pattern):
    rx = re.compile(pattern, re.I)
    return lambda title, rec: bool(rx.search(title))


TITLE_RULES = {
    "Soup": _t(r"\b(soup|broth|chowder|bisque|gazpacho|consomm)"),
    "Stew": _t(r"\b(stew|chili|chilli|tagine|goulash|ragout|gumbo|cassoulet)\b"),
    "Cake": lambda title, rec: bool(re.search(r"\b(cakes?|cupcakes?|cheesecakes?|torte|gateau|bundt)\b", title, re.I))
        and not re.search(r"pancake|crab|fish|rice cake|potato|salmon|tuna|corn cake|cookies|savou?ry", title, re.I)
        and rec["cat"] in ("Desserts", "Breads", "Breakfast & Brunch"),
    "Muffin": _t(r"\bmuffins?\b"),
    "Cookies": lambda title, rec: bool(re.search(r"\b(cookies?|biscotti|snickerdoodles?|macaroons?)\b", title, re.I)
        and not re.search(r"cookie (salad|butter|dough dip)", title, re.I))
        or (rec["cat"] == "Desserts" and bool(re.search(r"\bbiscuits?\b", title, re.I))),
    "Bread": lambda title, rec: rec["cat"] == "Breads" and bool(re.search(
        r"\b(bread|loaf|rolls?|buns?|bagels?|flatbread|focaccia|naan|pitas?|scones?|biscuits?|cornbread|baguette|brioche|challah)\b", title, re.I)),
    "Pie": lambda title, rec: bool(re.search(r"\b(pies?|tarts?|tartlets?|galette)\b", title, re.I))
        and not re.search(r"shepherd|cottage|pot pie|pizza|pie crust", title, re.I),
    "Stir-fry": _t(r"stir[- ]?fr(y|ied|ies)"),
}

MEAT = re.compile(
    r"\b(beef|steak|veal|lamb|mutton|goat|camel|chicken|turkey|duck|goose|quail|pigeon|meat(?!less| ?free| substitute)|mince(?!d)|"
    r"burger(?! bun)|sausages?|hot ?dogs?|liver|kidneys?(?! beans?)|bacon|ham|pork|salami|pepperoni|chorizo|prosciutto|pastrami|corned|jerky|"
    r"fish|salmon|tuna|cod|haddock|tilapia|trout|mackerel|sardines?|anchov|herring|halibut|snapper|sea ?bass|bream|catfish|pollock|swordfish|mahi|"
    r"shrimps?|prawns?|crab|lobster|scallops?|clams?|mussels?|oysters?|squid|calamari|octopus|seafood|surimi|"
    r"gelatin|gelatine|lard|suet|dripping|worcestershire|fish sauce|oyster sauce|shrimp paste|bonito|dashi|"
    r"brisket|sirloin|chuck|tenderloin|roast(?!ed|ing)|spare ?ribs|short ribs|rib ?eye|wings?|drumsticks?|thighs?|fillets?|cutlets?|chops?(?!p)|"
    r"marshmallows?(?! cr[eè]me| fluff))\w*", re.I)
VEG_OK = re.compile(r"\b(vegetarian|vegan|plant[- ]based|meatless|meat[- ]free|"
                    r"vegetable (stock|broth|bouillon)|goat'?s?’?s? (cheese|milk|curd)|beef ?(steak )?tomato|steak seasoning|chicken seasoning|"
                    r"turkey seasoning|fish seasoning)\b", re.I)
STOCK = re.compile(r"\b(stock|broth|bouillon)\b", re.I)


FISH = re.compile(r"\w+fish\b", re.I)   # monkfish, catfish, swordfish, shellfish


def vegetarian(lines, title=""):
    if MEAT.search(VEG_OK.sub(" ", title)) or FISH.search(title):
        return False
    for line in lines:
        rest = VEG_OK.sub(" ", line)       # "chicken or vegetable broth": the chicken still counts
        if MEAT.search(rest) or FISH.search(rest) or STOCK.search(rest):
            return False
    return True


def derive(rec, lines, times):
    title = rec["t"]["en"]["title"]
    out = {t for t, f in TITLE_RULES.items() if f(title, rec)}
    if sum(1 for x in lines if x.strip()) <= 5:
        out.add("5 or less ingredients")
    m = total_minutes(*times)
    if m is not None and m <= 30:
        out.add("Quick")
    if rec["cat"] in MAINS and "Vegetarian" in rec["diet"] and (rec["n"][0] or 0) >= 250 and (rec["n"][1] or 0) >= 10:
        out.add("Meatless Entree")
    return out


def apply(recipes, times_of):
    """Add derived dish tags (and Vegetarian); return {tag: added} and agreement with DaVita/ADA tags."""
    added, agree = {}, {}
    ref = {"DaVita", "Diabetes Food Hub (ADA)"}
    for rec in recipes:
        en = rec["t"].get("en")
        if not en:
            continue
        lines = [x[1] for x in en["ing"] if x[1]]
        if "Vegetarian" not in rec["diet"] and lines and vegetarian(lines, en["title"]):
            rec["diet"] = sorted(set(rec["diet"]) | {"Vegetarian"})
            added["Vegetarian"] = added.get("Vegetarian", 0) + 1
        new = derive(rec, lines, times_of(rec["id"]))
        if rec["sourceName"] in ref and rec["dish"]:
            for t in new | set(rec["dish"]):
                a = agree.setdefault(t, [0, 0])
                if t in rec["dish"]:
                    a[1] += 1
                    a[0] += t in new
        for t in new - set(rec["dish"]):
            added[t] = added.get(t, 0) + 1
        rec["dish"] = sorted(set(rec["dish"]) | new)
    return added, {t: round(100 * a / b) for t, (a, b) in agree.items() if b and t in TITLE_RULES.keys() | {"5 or less ingredients", "Quick", "Meatless Entree"}}
