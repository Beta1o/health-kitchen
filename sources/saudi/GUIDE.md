# Healthy Saudi recipes: writer's guide

Goal: for each dish in `dishes.json`, write ONE complete, healthier home recipe that is still the real dish, in Arabic and English, with nutrition computed from USDA data. These recipes are for people with kidney disease, diabetes, high blood pressure and heart disease, and for general healthy eating.

## 1. Research and validate (every dish)
1. Read the dish's encyclopediacooking pages (`urls` in dishes.json, pages are windows-1256; decode with `iconv -f windows-1256 -t utf-8` or Python `.decode("windows-1256")`). Use at most the first 3 URLs. Cache them under `sources/saudi/cache/` (file name = lesson number). These pages are the starting reference.
2. Validate with at least TWO other independent sources found with WebSearch/WebFetch (e.g. Arabic Wikipedia, Saudi Ministry of Culture / Saudi cuisine pages, reputable Arabic or English recipe sites such as sayidaty, fatafeat, arabnews, the Saudi culinary arts commission). Confirm: what the dish is, its region, its core ingredients and the cooking method. If sources disagree, follow the majority and the traditional core.
3. If you cannot validate a dish (too obscure, or sources contradict), skip it and list it in your reply with the reason. Never invent a dish.
4. Write the text yourself. Do not copy sentences from any site.

## 2. Make it healthier (keep the dish recognisable)
- Salt: no stock cubes, bouillon powder or ready seasoning salts. Use homemade unsalted stock. At most ¼ tsp (1.5 g) salt per serving in total; flavour with Saudi spices (bezar, cumin, coriander, cardamom, black lime/loomi, cinnamon, cloves, saffron, garlic, onion, herbs, lemon).
- Fat: use olive oil or a small amount of ghee (max 1 tsp ghee per serving) instead of large amounts; total added fat ≤ 1 tbsp (15 ml) per 2 servings. Trim visible fat from meat; skinless chicken.
- Meat: lean cuts, 90–120 g cooked meat/chicken/fish per serving.
- Grains: rice max ~150 g cooked per serving (about ¾ cup); prefer basmati or a mix with brown rice / whole wheat (jareesh, freekeh are already whole grain). More vegetables in the pot.
- Sugar: sweets and drinks use dates or a small amount of honey/sugar; cut sugar by at least half versus traditional; dessert portions small. Mark the sugar/honey/date-syrup lines as added sugar in the calc file.
- Frying: bake, grill, air-fry or pan-cook with little oil instead of deep frying.
- Dairy: low-fat laban/yoghurt/milk where it does not ruin the dish.
- Kidney-friendly notes (in hints): which ingredients are high in potassium or phosphorus (tomato paste, potatoes, dried legumes, dairy, nuts) and how to reduce them (smaller amount, leaching potatoes, rinsing canned legumes), and the portion to keep.
- Diabetes notes (in hints): carb portion, pairing with salad/vegetables, whole grains.
- No pork, no gelatin, no alcohol of any kind (also not in names: never call a drink "champagne"; use "sparkling apple drink" etc.).

## 3. Units and amounts
Metric only: g, kg, ml, l, tsp/tbsp (5/15 ml), °C, pieces (e.g. "2 medium onions (220 g)"). Give grams for every main ingredient so the nutrition can be computed. Portions: realistic household count (4–6 for mains). "Whole lamb / whole goat" dishes: scale to a home version with ~600 g meat, and say so in the description.

## 4. Nutrition (per serving)
Use `python3 nutrition/usda.py search <words>` to find foods (SR Legacy) and `python3 nutrition/usda.py calc <file>` to compute. For each recipe write `sources/saudi/calc/<id>.json`:
`{"servings": 4, "items": [{"fdc": 168878, "g": 600, "name": "cooked basmati rice"}, {"fdc": 169655, "g": 20, "added_sugar": true, "name": "honey"}]}`
Rules: raw weight for raw-listed foods; use "cooked" entries for rice/grains only if the amount in the recipe is cooked weight (prefer raw dry weight with the raw entry). Include oil, ghee, salt (salt, table: fdc 173468), dairy, dates, nuts — everything except water and whole spices. Use the closest generic food (e.g. lamb leg lean raw, chicken breast raw, onions raw, tomatoes raw, tomato paste canned no salt added). Copy the calc output numbers into `nutrients` (calories, protein_g, carbohydrates_g, fat_g, cholesterol_mg, sodium_mg, potassium_mg, phosphorus_mg, calcium_mg, fiber_g, added_sugar_g). Sanity-check the result (e.g. a kabsa serving ~450–650 kcal; a date sweet piece ~80–150 kcal); if it looks wrong, fix weights or fdc ids.

## 5. Output
Write `sources/saudi/out/<batch>.json`: a JSON array with TWO records per dish (Arabic first, then English), following `sources/FORMAT.md`:
- `source`: "saudi", `source_name`: "Saudi Kitchen (Health Kitchen)", `source_id`: "<id>" for Arabic and "<id>-en" for English; English has `"translation_of": "<id>"`.
- `url`: the first encyclopediacooking URL of the dish (the reference). `lang`: "ar" / "en".
- `title`: the dish name (Arabic: e.g. "كبسة الدجاج الصحية"; English: "Healthy Chicken Kabsa"). Plain, descriptive, no chef names.
- `description`: 1–3 sentences: what the dish is, its region, and what was made healthier.
- `portions`: "4"; `serving_size`: e.g. "1 plate (350 g)" / "طبق (350 غ)".
- `category`: one of the 14 categories in FORMAT.md; `cuisine`: ["Saudi"]; `dish`/`method` from FORMAT.md lists where they fit; `diet`: [] (diet tags are added later from the numbers).
- `ingredients`: [[group or null, line]] with grams; `steps`: [[null, step]] clear numbered actions (no numbers in text needed); `hints`: health notes (what changed vs traditional; kidney tip; diabetes tip), plus one final hint "References: <2–3 source names>" (names only).
- `nutrients`: from your calc (same numbers in both languages); `nutrients_raw`: null; images null; times as ISO 8601 (e.g. "PT45M") if known.
The Arabic and English versions must say the same thing (same ingredients, amounts, steps, hints in the same order and count).

## 6. Check before finishing
`python3 sources/saudi/check.py <batch>` must print OK.
