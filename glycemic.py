#!/usr/bin/env python3
"""Glycemic index (GI) and glycemic load (GL) of each recipe, and the ingredient lines that raise blood sugar most.

  python3 glycemic.py            # report on the database (coverage, low/medium/high counts, unmatched carb lines)
  python3 glycemic.py --foods    # the GI database foods behind every ingredient group, with their median GI

GI values come from the University of Sydney GI database (nutrition/gi_sydney.json, from
nutrition/gi_sydney.py; © GI News, University of Sydney, https://glycemicindex.com). Each ingredient group
below takes the median GI of the database foods its pattern matches, so one unusual test does not decide it.
Available carbohydrate per 100 g (carbohydrate minus fiber) is from USDA SR Legacy (nutrition/usda.db).

A recipe's GI is the carbohydrate-weighted average of its ingredients' GI (the method used for mixed meals,
Wolever 1986 / ISO 26642). Fat, protein, acid and cooking change the real value, so it is shown as an
estimate. GL per serving = GI x available carbohydrate per serving / 100, using the recipe's published
carbohydrate. Bands (Atkinson, Foster-Powell & Brand-Miller, Diabetes Care 2008 and 2021):
GI low <= 55, medium 56-69, high >= 70; GL per serving low <= 10, medium 11-19, high >= 20.
"""
import json
import re
import sqlite3
import statistics
import sys
from pathlib import Path

from shopping import parse

HERE = Path(__file__).resolve().parent
GI_FILE = HERE / "nutrition" / "gi_sydney.json"   # not in the repository (University of Sydney data); made by nutrition/gi_sydney.py
if not GI_FILE.exists():
    sys.exit("glycemic: nutrition/gi_sydney.json is missing, run python3 nutrition/gi_sydney.py first")
FOODS = json.loads(GI_FILE.read_text(encoding="utf-8"))["foods"]

# (group, ingredient line pattern, GI database name pattern, exclusions, available carbs g/100 g, g per ml, g per piece)
# First match wins, so specific lines come before general ones. A group with no GI pattern carries no sugar
# load (sweeteners, nut milks) and stops a later group from claiming the line.
NONE = None
GROUPS = [
    # no glycemic carbohydrate
    ("none", r"sugar[- ]free|spaghetti squash|zucchini (noodle|spiral|ribbon)|courgetti|zoodle|veg(etable|gie)? (noodle|rice)|cauliflower \W?rice|broccoli \W?rice|spaghetti mix|konjac|shirataki|palmini|hearts? of palm|bell peppers?|sweet peppers?|substitute|sweetener|stevia|splenda|erythritol|monk ?fruit|xylitol|sucralose|"
             r"\b(almond|coconut|cashew|hemp|macadamia|flax) (milk|beverage|cream|yogh?urt)|coconut (flake|water)|"
             r"cream of tartar|vinegar|extract|\bzest\b|\brind\b|\bpeel\b|\bvinaigrette\b|seasoning|cauliflower rice|"
             r"\blemons?\b|\blimes?\b|rice paper|cocoa|baking (powder|soda)|peppercorn|\byeast\b|potato starch|almond flour|"
             r"ground almond|coconut flour|nutritional|protein powder|renastep|\bstock\b|\bbroth\b|cooking spray",
     NONE, NONE, 0, 1, None),
    # sugars and syrups
    ("agave", r"\bagave\b", r"agave", NONE, 76.2, 1.39, None),
    ("honey", r"\bhoney\b", r"^honey,? (ns|pure|blend|\(|commercial|[a-z]+ ?(honey|tree|blossom|gum|box))|^honey$|honey, ",
     r"cereal|goldies|smacks|bubbles|puffs|snack|bar\b|loops|oat|nut|muesli|flakes|bran|rice|weet|joy|yog", 82.2, 1.42, None),
    ("maple syrup", r"^(?!.*\bin (extra )?(light |heavy )?syrup)(?=.*(maple syrup|\bsyrup\b))", r"maple syrup", NONE, 67.0, 1.32, None),
    ("coconut sugar", r"coconut (palm )?sugar|palm sugar|jaggery", r"coconut sugar|coconut palm sugar", NONE, 90.0, 0.6, None),
    ("molasses", r"molasse|date syrup|treacle|pomegranate molasses|silan|dibs", r"^(golden syrup|treacle|molasses)", NONE, 74.7, 1.4, None),
    ("jam", r"\bjam\b|preserves|marmalade|fruit spread|\bjelly\b", r"^jam|fruit spread|^marmalade|^strawberry jam|apricot jam",
     NONE, 67.8, 1.35, None),
    ("brown sugar", r"brown sugar|demerara|muscovado|turbinado|raw sugar", r"^sucrose", NONE, 98.1, 0.93, None),
    ("powdered sugar", r"(powdered|icing|confectioner'?s?) sugar", r"^sucrose", NONE, 99.8, 0.51, None),
    ("sugar", r"^(?!.*(no[- ]added[- ]sugar|no[- ]sugar|low[- ]sugar|reduced[- ]sugar|less[- ]sugar|sugar[- ]snap|unsweetened|without sugar))(?=.*\bsugar\b)", r"^sucrose", NONE, 99.9, 0.85, None),
    # flours, starches and crumbs (GI of the baked or cooked food they make)
    ("cornstarch", r"corn ?starch|cornflour|arrowroot", r"^100% waxy corn starch|^waxy maize .*starch.*(cooked|gel)|^modified cornstarch thickener", NONE,
     90.4, 0.54, None),
    ("tapioca", r"tapioca", r"^tapioca", NONE, 87.8, 0.51, None),
    ("rice flour", r"rice flour", r"^white rice|^rice, white", r"bread|cake|milk|flour|bran|syrup|puff|cracker|glutinous|parboiled|resistant|cooled|reheated", 77.7, 0.67, None),
    ("chickpea flour", r"(chickpea|gram|garbanzo) flour|besan", r"chickpea flour|besan", NONE, 47.0, 0.39, None),
    ("oat flour", r"oat flour", r"porridge|rolled oats", r"instant|sachet|flavou?r|honey|apple|fruit|bar\b|bread|biscuit|cookie|cake|drink|milk|barley|rice|millet|corn|semolina|buckwheat|sorghum|maize",
     59.2, 0.38, None),
    ("semolina", r"semolina|farina|cream of wheat", r"^semolina", r"gram|dhal|bread|pasta|pudding|khabisa", 68.9, 0.71, None),
    ("cornmeal", r"cornmeal|polenta|grits|masa", r"^cornmeal|^polenta|^corn meal", r"taco", 75.6, 0.65, None),
    ("wholemeal flour", r"(whole ?meal|whole ?wheat|wholewheat|whole grain|wholegrain|spelt|atta) (flour|pastry flour)|chapati flour",
     r"^(wholemeal|whole ?wheat|wholegrain) (bread|flour bread)|^bread, (wholemeal|whole ?wheat)", r"gluten|seed|grain|rye|soy|oat|fruit|raisin",
     61.3, 0.51, None),
    ("flour", r"\bflour\b", r"^white (wheat )?bread|^bread, white|^wonder white", r"gluten|fibre|fiber|added|\+|%|soy|seed|grain|resistant|vinegar|lupin|barley|oat|bean|spread|butter|jam",
     73.6, 0.53, None),
    ("graham crumbs", r"graham|digestive biscuit|cracker crumb", r"graham wafer|digestive|^crackers?,? (plain|water|wheat)|cream cracker", NONE, 73.4, 0.36, 7),
    ("breadcrumbs", r"bread ?crumb|panko|croutons?|stuffing", r"^white (wheat )?bread|^bread, white", r"gluten|fibre|fiber|added|\+|%|soy|seed|grain|resistant|vinegar|lupin|barley|oat|bean|spread|butter|jam",
     67.5, 0.35, None),
    ("crackers", r"crackers?|crispbread|rice cakes?|matzo", r"^crackers?\b|cracker, |^water crackers?|^crispbread|^rice cakes?", r"seed|cheese|bbq|pizza|shapes",
     73.0, 0.3, 7),
    ("chips", r"^(?!.*(chocolate|choc|carob))(?=.*(\bchips\b|crisps\b|pretzels?|popcorn))|^(?!.*(chocolate|choc|carob)).*\bchips\b|crisps\b|pretzels?|popcorn", r"^(corn|tortilla) chips|^potato crisps|^pretzels?|^popcorn", r"flax|bean|lentil|vegetable|apple|banana", 55.0, 0.1, 2),
    # breads
    ("tortilla corn", r"corn tortilla|tortillas?,? corn|taco shell|tostada", r"^corn tortilla|^tortilla, corn|taco shell", r"taco,|served|fried|with|potato|bean", 38.3, None, 26),
    ("tortilla", r"tortilla|\bwraps?\b|lavash|chapati|roti|paratha", r"^wheat tortilla|^tortilla, wheat|^flour tortilla|^(white|wholemeal) wrap|^wrap|chapat|^roti",
     r"chip|corn|soy|lupin|protein|low.carb", 45.9, None, 45),
    ("pita wholemeal", r"(whole ?wheat|whole ?meal|whole ?grain|wholegrain).*\b(pita|pitta)", r"(pita|lebanese).*(wholemeal|whole)", NONE, 47.6, None, 64),
    ("pita", r"\b(pita|pitta|khubz|lebanese bread|flatbread|naan)\b", r"^pita|^lebanese bread|^naan|^flatbread", r"wholemeal|hummus|falafel|sandwich|naankhatai|consumed|curry", 53.5, None, 60),
    ("bagel", r"bagel|english muffin|crumpet", r"^bagel|^english muffin|^crumpet", NONE, 47.0, None, 70),
    ("bun", r"\bbuns?\b|\brolls?\b(?!.*(oat|cabbage|grape))|baguette|ciabatta|brioche|croissant|hoagie|kaiser",
     r"^(hamburger |bread |white )?(bun|roll)s?\b|^baguette|^bread roll|^kaiser", r"sweet|cinnamon|hot cross|fruit|spring roll|sushi", 47.4, None, 50),
    ("bread wholemeal", r"(whole ?wheat|whole ?meal|wholewheat|whole ?grain|wholegrain|multigrain|granary|rye|seeded|sprouted|oat|bran|brown).*\bbread\b",
     r"^(wholemeal|whole ?wheat|wholegrain|whole grain|multigrain|mixed grain|rye) bread|^bread, (wholemeal|whole ?wheat|wholegrain|rye|mixed grain)",
     r"gluten|lupin|soy|%|\+|fruit|raisin|spread|juice|vinegar", 37.0, 0.25, 33),
    ("bread", r"\bbread\b|\btoast\b|sourdough", r"^white (wheat )?bread|^bread, white|^wonder white",
     r"gluten|fibre|fiber|added|\+|%|soy|seed|grain|resistant|vinegar|lupin|barley|oat|bean|spread|butter|jam", 46.7, 0.25, 28),
    # grains, cooked (line says cooked) and dry
    ("brown rice cooked", r"(brown|wild|red|black) (basmati )?rice.*(?<!un)cooked|(?<!un)cooked.*(brown|wild|red|black) (basmati )?rice", r"^brown rice|^rice, brown|brown basmati", r"bread|cake|milk|quinoa|cracker|noodle|pasta|flour|bran|syrup|puff|chip|beverage|drink",
     21.2, 0.82, None),
    ("brown rice", r"brown (basmati )?rice|wild rice|red rice|black rice", r"^brown rice|^rice, brown|brown basmati", r"bread|cake|milk|quinoa|cracker|noodle|pasta|flour|bran|syrup|puff|chip|beverage|drink",
     72.7, 0.81, None),
    ("basmati cooked", r"basmati.*(?<!un)cooked|(?<!un)cooked.*basmati", r"^basmati|basmati rice|rice, basmati", r"brown|pila[fu]|with|consumed|chicken|arseyah", 27.8, 0.67, None),
    ("basmati", r"basmati|long[- ]grain|sella", r"^basmati|basmati rice|rice, basmati", r"brown|pila[fu]|with|consumed|chicken|arseyah", 78.7, 0.79, None),
    ("jasmine cooked", r"jasmine.*(?<!un)cooked|(?<!un)cooked.*jasmine|sticky rice.*(?<!un)cooked", r"jasmine", r"brown", 27.8, 0.67, None),
    ("jasmine", r"jasmine|sticky rice|glutinous rice|sushi rice|short[- ]grain", r"jasmine", r"brown", 78.7, 0.79, None),
    ("arborio", r"arborio|risotto|carnaroli", r"arborio|risotto rice|carnaroli", NONE, 78.7, 0.79, None),
    ("rice noodles cooked", r"(rice (noodle|vermicelli|stick)|vermicelli|pad thai noodle).*((?<!un)cooked|ready|fresh|soaked)|((?<!un)cooked|ready[- ]to|fresh).*(rice noodle|vermicelli)",
     r"rice noodle|rice vermicelli|^vermicelli|mung bean noodle", NONE, 23.0, 0.6, None),
    ("rice noodles", r"rice (noodle|vermicelli|stick)|vermicelli|pad thai noodle|glass noodle|cellophane", r"rice noodle|rice vermicelli|^vermicelli|mung bean noodle",
     NONE, 78.4, 0.4, None),
    ("rice cooked", r"\brice\b.*((?<!un)cooked|leftover|steamed|boiled)|((?<!un)cooked|leftover|steamed|boiled).*\brice\b", r"^white rice|^rice, white", r"bread|cake|milk|flour|bran|syrup|puff|cracker|glutinous|parboiled|resistant|cooled|reheated",
     27.8, 0.67, None),
    ("rice", r"\brice\b(?!.*(vinegar|wine|milk|cake|bran|syrup|cracker|krispies|puff))", r"^white rice|^rice, white", r"bread|cake|milk|flour|bran|syrup|puff|cracker|glutinous|parboiled|resistant|cooled|reheated",
     78.7, 0.79, None),
    ("pasta wholemeal cooked", r"(whole ?wheat|whole ?meal|whole ?grain|wholegrain|brown rice).*(pasta|spaghetti|penne|macaroni|noodle|fusilli|rotini|linguine|lasagn).*(?<!un)cooked|(?<!un)cooked.*(whole ?wheat|wholemeal|whole ?grain).*(pasta|spaghetti|penne|macaroni|noodle)",
     r"^(spaghetti|pasta|penne|fusilli|macaroni),? (whole ?meal|whole ?wheat|whole ?grain)|^(whole ?meal|whole ?wheat|wholegrain) (spaghetti|pasta|penne)", NONE, 22.0, 0.59, None),
    ("pasta wholemeal", r"(whole ?wheat|whole ?meal|whole ?grain|wholegrain|brown rice|lentil|chickpea|bean).*(pasta|spaghetti|penne|macaroni|noodle|fusilli|rotini|linguine|lasagn|elbow|orzo)",
     r"^(spaghetti|pasta|penne|fusilli|macaroni),? (whole ?meal|whole ?wheat|whole ?grain)|^(whole ?meal|whole ?wheat|wholegrain) (spaghetti|pasta|penne)", NONE, 65.0, 0.42, None),
    ("pasta cooked", r"(pasta|spaghetti|penne|macaroni|noodle|fusilli|rotini|linguine|fettuccine|farfalle|lasagn|elbow|orzo|ziti|rigatoni|shells|tagliatelle|gnocchi|tortellini|ravioli).*(?<!un)cooked|(?<!un)cooked.*(pasta|spaghetti|penne|macaroni|noodle|fusilli|rotini|orzo)",
     r"^(spaghetti|penne|fusilli|macaroni|linguine|fettuccine|rigatoni|pasta)\b", r"gluten|whole|wholemeal|sauce|canned|tinned|rice|corn|bean|lentil|pea|soy|lupin|protein|vegetable|cheese|instant|puree|tomato|baby|bolognese|cooked.*cooled",
     29.1, 0.59, None),
    ("egg noodles", r"egg noodle|ramen|udon|soba|lo mein|instant noodle|chow mein", r"^(wheat (\(egg\) )?noodles?|noodles, (wheat|made from wheat)|udon|soba|ramyeon|hokkien|instant .?two-minute|instant noodles|buckwheat noodles)", r"broth|soup|anchovy|sauce|okara|fried|chicken|served", 68.0, 0.38, None),
    ("pasta", r"\b(pasta|spaghetti|penne|macaroni|noodles?|fusilli|rotini|linguine|fettuccine|farfalle|lasagn[ae]|elbows?|orzo|ziti|rigatoni|shells|tagliatelle|gnocchi|tortellini|ravioli|vermicelli)\b",
     r"^(spaghetti|penne|fusilli|macaroni|linguine|fettuccine|rigatoni|pasta)\b", r"gluten|whole|wholemeal|sauce|canned|tinned|rice|corn|bean|lentil|pea|soy|lupin|protein|vegetable|cheese|instant|puree|tomato|baby|bolognese|cooked.*cooled",
     71.8, 0.42, None),
    ("couscous cooked", r"couscous.*(?<!un)cooked|(?<!un)cooked.*couscous", r"^couscous|^pearl couscous", r"soup", 21.8, 0.66, None),
    ("couscous", r"couscous|freekeh|farro|kamut|wheat berr|cracked wheat", r"^couscous|^pearl couscous", r"soup", 72.4, 0.73, None),
    ("bulgur cooked", r"(bulgur|bulghur|burghul).*(?<!un)cooked|(?<!un)cooked.*(bulgur|bulghur)", r"^bulgur|^burghul", NONE, 14.1, 0.77, None),
    ("bulgur", r"bulgur|bulghur|burghul", r"^bulgur|^burghul", NONE, 63.4, 0.59, None),
    ("quinoa cooked", r"quinoa.*(?<!un)cooked|(?<!un)cooked.*quinoa", r"^quinoa", r"milk|drink|wrap|porridge|retort", 18.5, 0.78, None),
    ("quinoa", r"quinoa|millet|buckwheat|amaranth|sorghum|teff", r"^quinoa", r"milk|drink|wrap|porridge|retort", 57.2, 0.72, None),
    ("barley cooked", r"barley.*(?<!un)cooked|(?<!un)cooked.*barley", r"^pearl barley|^barley, pearl", NONE, 24.4, 0.66, None),
    ("barley", r"barley", r"^pearl barley|^barley, pearl", NONE, 62.1, 0.84, None),
    ("oatmeal cooked", r"(oatmeal|porridge|oats).*((?<!un)cooked|prepared)|(?<!un)cooked (oatmeal|oats|porridge)", r"porridge|rolled oats", r"instant|sachet|flavou?r|honey|apple|fruit|bar\b|bread|biscuit|cookie|cake|drink|milk|barley|rice|millet|corn|semolina|buckwheat|sorghum|maize",
     10.3, 0.99, None),
    ("instant oats", r"(instant|quick[- ]cook(ing)?|quick) (oat|oatmeal|porridge)", r"instant (oat|porridge)|quick oats|quick.cook", r"flavou?r|honey|apple|fruit|bar\b|maple|choc|berry|cinnamon|banana",
     57.6, 0.34, None),
    ("steel-cut oats", r"steel[- ]cut|pinhead|oat groats|scottish oats", r"steel.cut|oat groats|pinhead", NONE, 57.6, 0.68, None),
    ("oats", r"\boats?\b|oatmeal|porridge|muesli|granola|oat bran", r"porridge|rolled oats", r"instant|sachet|flavou?r|honey|apple|fruit|bar\b|bread|biscuit|cookie|cake|drink|milk|barley|rice|millet|corn|semolina|buckwheat|sorghum|maize",
     57.6, 0.34, None),
    # starchy vegetables
    ("sweet potato", r"sweet potato|\byams?\b", r"^sweet potato", r"puree|chip|fries|crisp|mash.*commercial|vegetable|pumpkin|baby|soup", 17.1, 0.56, 130),
    ("new potato", r"(new|baby|fingerling|salad|charlotte) potato|potatoes,? (new|baby)", r"new potato|baby potato|potato.*(new|baby|chats)", NONE, 15.4, 0.63, 60),
    ("potato", r"\bpotato(es)?\b(?!.*chip)|hash brown", r"^potato(es)?,? .*(boiled|baked|mashed|roasted|microwaved|steamed)|^(boiled|baked|mashed) potato",
     r"instant|chip|crisp|puree|salad|soup|french|fries|flake|cooled|reheated|vinegar|starch|wedge|frozen|canned|tinned|sweet|new|baby|pasta",
     15.4, 0.63, 213),
    ("corn", r"\b(sweet ?corn|corn kernels?|corn on the cob|ears? of corn|corn)\b(?!.*(starch|flour|meal|syrup|tortilla|oil|flake|chip))", r"^sweet ?corn|^corn, sweet|^corn on the cob|maize, sweet",
     r"rice|baby|soup|chip|flake|cream", 17.0, 0.65, 90),
    ("peas", r"(?<!chick)(?<!snow )(?<!snap )(?<!split )(?<!sugar snap )\bpeas?\b(?!.*(protein|shoot|pod))", r"^(green )?peas\b|^peas,", r"split|dried|soup|chick|pigeon|yellow",
     9.1, 0.61, None),
    ("carrot", r"carrots?\b", r"^carrots?,? ", r"cake|juice|muffin|soup|puree", 6.8, 0.54, 61),
    ("parsnip", r"parsnip", r"parsnip", NONE, 13.1, 0.56, 130),
    ("beet", r"\bbeets?\b|beetroot", r"beetroot|^beets", NONE, 6.8, 0.57, 82),
    ("pumpkin puree", r"pumpkin (puree|pur e|purée)|canned pumpkin|pumpkin, canned|tin(ned)? pumpkin", r"^pumpkin,? |^butternut", r"seed|bread|cob|cracker|soup|puree|scone|muffin",
     5.2, 1.0, None),
    ("pumpkin", r"pumpkin(?! (seed|pie spice|spice))|butternut|acorn squash|kabocha|squash(?!.*(spaghetti|zucchini|yellow|summer))", r"^pumpkin,? |^butternut", r"seed|bread|cob|cracker|soup|puree|scone|muffin",
     8.0, 0.59, None),
    ("plantain", r"plantain", r"plantain", NONE, 29.6, 0.6, 180),
    ("cassava", r"cassava|yuca|taro|eddoe", r"cassava|taro", r"chip|flour|bread", 36.0, 0.6, None),
    # legumes
    ("lentils cooked", r"lentils?.*((?<!un)cooked|canned|tinned|can|tin|drained)|((?<!un)cooked|canned|tinned).*lentils?|\d+\s*(x\s*)?\d*\s*g? ?(cans?|tins?) .*lentil", r"^lentils?\b|^(red|green|brown) lentils", r"soup|puree|muffin|pasta|flour|bread|cracker|chip|snack|vegetable",
     12.2, 0.84, None),
    ("lentils", r"lentils?|\bdal\b|\bdhal\b|\bmasoor\b|\btoor\b", r"^lentils?\b|^(red|green|brown) lentils", r"soup|puree|muffin|pasta|flour|bread|cracker|chip|snack|vegetable",
     52.7, 0.81, None),
    ("split peas", r"split peas?|yellow peas", r"split peas|yellow peas", r"soup", 34.9, 0.83, None),
    ("chickpeas dry", r"^(?!.*\b(cans?|canned|tins?|tinned|cooked)\b).*((dried|dry) (chick ?peas?|garbanzo)|(chick ?peas?|garbanzo)[^(]*\b(dried|soaked))", r"^chick ?peas|^garbanzo|^bengal gram", r"flour|bread|roasted|snack|chip|puree|hummus|curry",
     44.0, 0.82, None),
    ("chickpeas", r"chick ?peas?|garbanzo|chana", r"^chick ?peas|^garbanzo|^bengal gram", r"flour|bread|roasted|snack|chip|puree|hummus|curry", 19.8, 0.69, None),
    ("hummus", r"hummus|houmous|humus", r"hummus|houmous", r"bread|falafel", 8.3, 1.0, None),
    ("baked beans", r"baked beans", r"^baked beans", NONE, 17.0, 1.0, None),
    ("beans dry", r"(dried|dry) (black|kidney|pinto|white|navy|cannellini|haricot|butter|lima|fava|broad|great northern|red|mung|adzuki|borlotti)? ?beans|beans.*(dried|dry|soaked overnight)",
     r"(kidney|black|pinto|navy|haricot|white|butter|lima|cannellini|borlotti|mung) beans?\b", r"baked|soup|chip|snack|noodle|sauce|paste|burrito|salad|sprout|green|vegetable",
     45.0, 0.8, None),
    ("beans", r"\b(black|kidney|pinto|white|navy|cannellini|haricot|butter|lima|fava|broad|great northern|red|mung|adzuki|borlotti|refried|mixed|black-eyed|cranberry) beans?\b|black-eyed peas|\bfoul\b|\bful\b|fava",
     r"(kidney|black|pinto|navy|haricot|white|butter|lima|cannellini|borlotti|mung|black.eyed) (beans?|peas)\b", r"baked|soup|chip|snack|noodle|sauce|paste|burrito|salad|sprout|green|vegetable",
     15.6, 0.72, None),
    # fruit juices before whole fruit
    ("orange juice", r"orange juice|juice (of )?(an |\d )?oranges?", r"^orange juice", r"beverage|drink|cordial", 10.2, 1.04, 86),
    ("apple juice", r"\bapple juice|\bapple cider(?! vinegar)", r"^apple juice", r"beverage|drink|cordial|blend|cloudy.*pear", 11.1, 1.04, None),
    ("pineapple juice", r"pineapple juice", r"^pineapple juice", NONE, 12.7, 1.05, None),
    ("fruit juice", r"(grape|cranberry|pomegranate|mango|cherry|grapefruit|fruit) juice|nectar", r"^(grapefruit|cranberry|tomato|pineapple|orange|apple) juice|juice cocktail",
     r"beverage|drink|cordial|tomato", 13.0, 1.04, None),
    ("applesauce", r"apple ?sauce|apple puree|stewed apple", r"^apples?,? (raw|golden|granny|red|green|fuji|gala|pink|braeburn|ns)|^apple$|^apples?$|apple, pear and cinnamon fruit puree, homemade", r"juice|dried|muffin|cake|bar|sauce|chips", 10.1, 1.03, None),
    ("apple", r"\bapples?\b", r"^apples?,? (raw|golden|granny|red|green|fuji|gala|pink|braeburn|ns)|^apple$|^apples?$", r"juice|dried|muffin|cake|bar|puree|sauce|chips",
     11.4, 0.53, 182),
    ("banana", r"bananas?", r"^bananas?,? |^banana$", r"cake|bread|muffin|smoothie|drink|chip|dried|flour|oat|cereal", 20.2, 0.95, 118),
    ("strawberries", r"strawberr", r"^strawberr(y|ies),? (raw|fresh|ns)|^strawberries$", r"jam|yog|ice|smoothie|drink|milk|muffin", 5.7, 0.64, 12),
    ("blueberries", r"blueberr|blackberr|raspberr|mixed berr|\bberries\b|boysenberr|mulberr", r"^(blueberr|raspberr|blackberr)(y|ies)\b", r"muffin|jam|yog|granola|bar|juice|drink|cereal|muesli|oat|spread|leather|sour buzz|cake",
     8.0, 0.62, None),
    ("cherries", r"cherr(y|ies)(?!.*tomato)", r"^cherries", r"tomato", 13.9, 0.65, 8),
    ("grapes", r"\bgrapes?\b(?!fruit)", r"^grapes", NONE, 17.2, 0.64, 5),
    ("orange", r"\boranges?\b|mandarin|clementine|tangerine|satsuma", r"^oranges?\b|^mandarin", r"juice|marmalade|cordial|drink|canned|cocktail|spread", 9.4, 0.76, 131),
    ("grapefruit", r"grapefruit", r"^grapefruit", r"juice", 8.0, 0.8, 250),
    ("pineapple canned", r"pineapple.*(canned|tinned|can|tin|in juice|in syrup)|(canned|tinned).*pineapple", r"pineapple.*canned|canned.*pineapple", r"peach", 14.9, 0.76, None),
    ("pineapple", r"pineapple", r"^pineapple,? (raw|fresh)|^pineapple$|^pineapple \(", r"juice|canned|yog", 11.7, 0.7, None),
    ("mango", r"mango", r"^mango,? |^mangoes|^mango$", r"smoothie|juice|ice|yog|drink|slice|bar|chutney|passion|dried", 13.4, 0.7, 200),
    ("pear", r"\bpears?\b", r"^pears?,? ", r"canned|juice|couscous", 12.1, 0.6, 178),
    ("peach canned", r"peach.*(canned|tinned|in syrup|in juice)|(canned|tinned).*peach", r"^peach.*canned|^peaches.*canned", r"pineapple|grape|pear", 13.3, 0.9, None),
    ("peach", r"peach|nectarine|apricots?(?!.*dried)|plums?\b", r"^peach\b|^peach \(|^peaches,? (raw|fresh)|^apricots?,? (raw|fresh|ns)|^plums?,? raw", r"canned|dried|jam|juice|palm|strip|chip|pear", 8.0, 0.65, 150),
    ("dates", r"\bdates?\b(?! syrup)|medjool", r"^dates,? ", r"bar|paste|syrup|ball|muffin|cake|cookie", 67.0, 0.62, 8),
    ("raisins", r"raisins?|sultanas?|(?<!red )(?<!black )(?<!white )\bcurrants?\b", r"^raisins?\b|^sultanas?\b|^currants?\b", r"bread|muffin|bran|cereal|bun|scone|toast|oat", 75.5, 0.61, None),
    ("dried cranberries", r"(dried|craisin).*cranberr|cranberr.*dried|craisins", r"^cranberries, sweetened, dried|^dried cranberr|craisin", NONE, 77.1, 0.51, None),
    ("dried apricots", r"dried apricot|apricots?,? dried|dried (fig|prune)|prunes?|\bfigs?\b", r"^apricots?,? dried|^dried apricot|^prunes?|^figs?,? dried", r"bar|snack", 55.3, 0.55, 8),
    ("watermelon", r"watermelon|cantaloupe|rockmelon|honeydew|\bmelon\b", r"^watermelon|^cantaloupe|^rockmelon", NONE, 7.2, 0.64, None),
    ("kiwi", r"kiwi", r"^kiwi", NONE, 11.7, 0.7, 70),
    ("pomegranate", r"pomegranate (seed|aril)|pomegranates?\b(?! molasses)", r"pomegranate juice", NONE, 14.7, 0.75, None),
    # dairy and dairy-style drinks
    ("rice milk", r"rice milk|rice drink|oat milk|oat drink|oat beverage", r"^rice milk|^oat milk|oat drink|oat beverage", NONE, 8.9, 1.0, None),
    ("soy milk", r"soy ?milk|soya milk|soy beverage|soya drink", r"^soy ?milk|^soya milk|soy milk beverage|soy beverage", r"choc|malt|flavou?r|banana|cereal|up & go|vanilla|coffee",
     3.0, 1.02, None),
    ("condensed milk", r"condensed milk", r"^milk, condensed", NONE, 54.4, 1.3, None),
    ("ice cream", r"ice cream|frozen yogh?urt|gelato|sorbet", r"^ice cream", NONE, 22.9, 0.56, None),
    ("yogurt", r"yogh?urt|yoghourt|laban|labneh|kefir|skyr", r"^yogh?urt,? (plain|natural|greek|low.fat, natural|reduced.fat, natural|unflavou?red|ns)|^(fat.free |low.fat |reduced.fat )?(natural|plain|greek)( style)? yogh?urt",
     r"fruit|vanilla|strawberr|honey|berry|choc|apricot|mango|peach|sweetened|flavou?r|drink|dates|eaten|consumed", 5.0, 1.04, None),
    ("milk", r"\bmilk\b(?!.*(chocolate|powder))|buttermilk", r"^milk,? (full.fat|whole|skim|reduced.fat|low.fat|semi.skimmed|fat.free|1%|2%|lite|light|ns|pasteuri)|^(skim|full.fat|whole|low.fat|reduced.fat|semi.skimmed) milk",
     r"choc|flavou?r|condensed|powder|malt|banana|strawberr|coffee|drink|evaporated|soy|rice|oat|almond|goat|camel|fermented|lactose|honey", 4.9, 1.03, None),
    ("chocolate", r"chocolate|cacao nibs|carob", r"^chocolate,? (dark|milk|plain|ns)|^dark chocolate|^milk chocolate", r"cake|muffin|drink|milk drink|biscuit|cookie|bar,|spread|mousse|pudding|raisin|peanut",
     50.0, 0.71, None),
]
COMPILED = []
for g, line, gi_rx, ex, carbs, dens, pc in GROUPS:
    gi = None
    if gi_rx:
        rx, xx = re.compile(gi_rx, re.I), re.compile(ex, re.I) if ex else None
        hits = [f for f in FOODS if rx.search(f["name"]) and not (xx and xx.search(f["name"]))]
        gi = (round(statistics.median(f["gi"] for f in hits)), hits) if hits else None
        if not hits:
            print(f"glycemic: no GI database food for group {g!r}", file=sys.stderr)
    COMPILED.append((g, re.compile(line, re.I), gi, carbs, dens, pc))
# non-starchy vegetables: little available carbohydrate and no measured GI, so they are left out of the GI average but
# count as explained carbohydrate when deciding whether a recipe's GI is well enough supported
# (pattern, available carbs g/100 g from USDA SR Legacy, g per ml, g per piece)
VEG = [(re.compile(p, re.I), c, d, pc) for p, c, d, pc in [
    (r"tomato (paste|pur[eé]e)|passata", 14.2, 1.1, None), (r"tomato sauce|marinara|salsa\b", 5.5, 1.0, None),
    (r"(canned|tinned|crushed|diced|chopped) tomato|tomatoes,? (canned|tinned)|tin(ned)? tomato", 3.0, 1.0, None),
    (r"cherry tomato|grape tomato", 2.7, .6, 17), (r"tomato", 2.7, .76, 123), (r"shallot", 13.8, .67, 25),
    (r"(green|spring) onion|scallion", 4.7, .4, 15), (r"\bonions?\b", 7.6, .67, 110), (r"\bleeks?\b", 12.3, .4, 89),
    (r"garlic", 31.0, .55, 3), (r"celery", 1.4, .5, 40), (r"cucumber", 3.1, .55, 300), (r"(bell|sweet) peppers?|capsicum|red pepper|green pepper|yellow pepper", 3.9, .62, 120),
    (r"spinach", 1.4, .2, None), (r"zucchini|courgette", 2.1, .52, 196), (r"mushroom", 2.3, .3, 18), (r"broccoli", 4.0, .38, None),
    (r"cauliflower", 3.0, .45, 575), (r"cabbage|coleslaw|slaw mix", 3.3, .37, None), (r"lettuce|kale|arugula|rocket|greens|chard|watercress", 1.5, .2, None),
    (r"green beans?|string beans?", 4.3, .5, None), (r"eggplant|aubergine", 2.9, .35, 458), (r"asparagus", 1.8, .6, 16), (r"okra", 4.3, .4, 12),
    (r"radish", 1.8, .5, 5), (r"jalape|chil(l)?i(es)? pepper|\bchil(l)?ies?\b", 6.0, .5, 14)]]
# sources whose published carbohydrate already excludes fiber (UK labelling); the rest list total carbohydrate
NET_CARB_SOURCES = {"Diabetes UK", "Kidney Care UK", "My Renal Nutrition"}
GI_BANDS, GL_BANDS = (55, 69), (10, 19)


# cooked, dry and canned forms of one food share its entry in the app's food guide
BASE = {"oatmeal cooked": "oats", "chickpeas dry": "chickpeas", "beans dry": "beans", "pumpkin puree": "pumpkin", "peach canned": "peach",
        "pineapple canned": "pineapple", "rice noodles cooked": "rice noodles"}


def base_group(g):
    return BASE.get(g) or (g[:-7] if g.endswith(" cooked") else g)


def group_of(line):
    low = line.lower()
    for g, rx, gi, carbs, dens, pc in COMPILED:
        if rx.search(low):
            return g, gi, carbs, dens, pc
    return None


SIZE = [(re.compile(r"\b(small|mini|baby)\b", re.I), .6), (re.compile(r"\b(large|big|jumbo)\b", re.I), 1.4)]


def grams(amt, unit, dens, pc, line=""):
    if amt is None:
        return None
    if unit == "pc" and pc:
        pc *= next((f for rx, f in SIZE if rx.search(line)), 1)
    if unit == "g":
        return amt
    if unit == "ml":
        return amt * dens if dens else None
    if unit == "pc":
        return amt * pc if pc else None
    return None


def band(v, cut):
    return None if v is None else 0 if v <= cut[0] else 1 if v <= cut[1] else 2


def recipe(lines, servings, carbs, fiber, source, portions=None):
    """{'gi', 'gl', 'gx': [[line position, GI, share of the sugar load %], ...]} or None, plus report details."""
    parts, unknown, unmatched, veg = [], [], [], 0.0
    for pos, line in enumerate(lines):
        p = parse(line)
        if not p:
            continue
        hit = group_of(line)
        if not hit or hit[1] is None:
            v = next((x for x in VEG if x[0].search(line)), None)
            if v:
                w = grams(p[0], p[1], v[2], v[3], line)
                if w:
                    veg += w * v[1] / 100
                continue
            if not hit:
                unmatched.append(p[2])
            continue
        g, gi, c100, dens, pc = hit
        w = grams(p[0], p[1], dens, pc, line)
        if w is None:
            unknown.append(g)
            continue
        parts.append((pos, g, gi[0], w * c100 / 100))
    total = sum(x[3] for x in parts)
    serv = servings or 1
    stated = None
    if carbs is not None:
        stated = carbs if source in NET_CARB_SOURCES else carbs - (fiber or 0)
        stated = max(stated, 0)
    if carbs is None and not re.fullmatch(r"\s*\d+\s*(portions?|servings?)?\s*", portions or ""):
        return None, {"est": 0, "stated": None, "unknown": unknown, "unmatched": unmatched, "parts": parts}   # no per-serving amount to go on
    est = total / serv
    avail = stated if stated is not None else (est if total else None)
    info = {"est": est, "stated": stated, "unknown": unknown, "unmatched": unmatched, "parts": parts}
    if avail is None:
        return None, info
    gi = round(sum(x[2] * x[3] for x in parts) / total) if total else None
    # a GI is shown only when the matched ingredients explain at least 70% of the published carbohydrate
    coverage = 1.0 if stated is None or stated < 1 else min(1.0, (est + veg / serv) / stated)
    covered = coverage >= 0.7
    if avail < 5:   # a few grams of carbohydrate: the load is low whatever the GI; without a GI, GL is given as its ceiling (GI 100)
        out = {"gl": round(avail * gi / 100, 1)} if gi is not None and covered else {"gl": round(avail, 1), "glMax": 1}
        if gi is not None and covered:
            out["gi"] = gi
    elif gi is None or not covered:
        return None, info
    else:
        out = {"gi": gi, "gl": round(gi * avail / 100, 1)}
    if "gi" in out:
        out["gc"] = round(coverage * 100)   # share of the published carbohydrate the matched ingredients explain
    load = sum(x[2] * x[3] for x in parts)
    gx = sorted(((x[0], x[2], round(x[2] * x[3] / load * 100)) for x in parts if load), key=lambda t: -t[2])
    gx = [list(t) for t in gx if t[2] >= 8][:5]
    # what leaving out an ingredient, or using half, would do: its carbohydrate leaves the serving and the GI is
    # recomputed from the rest; [.., GI without, GL without, GI with half, GL with half] (GI None: no other carb-rich ingredient)
    if avail >= 5 and gi is not None:
        for t in gx:
            mine = [x for x in parts if x[0] == t[0]]
            c = sum(x[3] for x in mine) / serv * (avail / est if est > avail else 1)   # this line's carbs per serving, never more than published
            def what_if(f):
                w = [(x[2], x[3] * (f if x[0] == t[0] else 1)) for x in parts]
                tot = sum(v for _, v in w)
                g2 = round(sum(a * v for a, v in w) / tot) if tot else None
                rest = max(0.0, avail - c * (1 - f))
                return g2, round((g2 if g2 is not None else 0) * rest / 100, 1) if g2 is not None else None
            t += [*what_if(0), *what_if(.5)]
    out["gx"] = gx
    return out, info


def report(db_path):
    from collections import Counter
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    rows = db.execute("SELECT id, portions, carbohydrates_g, fiber_g, source_name FROM recipes WHERE canonical_id = id").fetchall()
    n = len(rows)
    got, gis, gls, ratio, unmatched = 0, Counter(), Counter(), [], Counter()
    by_src = {}
    for r in rows:
        lines = [t for (t,) in db.execute("SELECT text FROM ingredients_i18n WHERE recipe_id=? AND lang='en' ORDER BY position", (r["id"],))]
        m = re.match(r"\s*(\d+)", r["portions"] or "")
        out, info = recipe(lines, int(m.group(1)) if m else None, r["carbohydrates_g"], r["fiber_g"], r["source_name"] or "DaVita", r["portions"])
        unmatched.update(info["unmatched"])
        src = r["source_name"] or "DaVita"
        if info["stated"] and info["stated"] >= 5:
            by_src.setdefault(src, []).append(info["est"] / info["stated"])
        if out:
            got += 1
            gis[band(out.get("gi"), GI_BANDS)] += 1
            gls[band(out["gl"], GL_BANDS)] += 1
    print(f"{got}/{n} recipes have a GL ({got / n:.0%}); GI bands low/med/high/none {[gis[0], gis[1], gis[2], gis[None]]}; "
          f"GL bands {[gls[0], gls[1], gls[2]]}")
    for s, v in sorted(by_src.items()):
        print(f"  {s}: matched/published carbs median {statistics.median(v):.2f} over {len(v)}")
    print("unmatched lines (top):", ", ".join(f"{k}:{c}" for k, c in unmatched.most_common(150)))


def foods():
    for g, rx, gi, carbs, dens, pc in COMPILED:
        if gi:
            names = sorted({f["name"][:60] for f in gi[1]})
            print(f"{g}: GI {gi[0]} (median of {len(gi[1])}) e.g. {' | '.join(names[:6])}")


if __name__ == "__main__":
    if "--foods" in sys.argv:
        foods()
    else:
        import os
        report(os.environ.get("HK_DB") or HERE / "davita_recipes.db")
