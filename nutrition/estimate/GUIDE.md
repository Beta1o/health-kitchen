# Estimating missing nutrients from the ingredient list (USDA SR Legacy)

Some publishers print no potassium, phosphorus, cholesterol or added sugar. For those recipes we compute the
nutrients from the ingredient list, and the build only uses an estimate when the computed calories, protein,
carbohydrate and sodium agree with the numbers the publisher did print (nutrition/estimate/merge.py).

## Your job
For every recipe in your input file, write one calc file `<out dir>/<id>.json`:

    {"id": 123, "servings": 4, "items": [
      {"line": 0, "fdc": 169756, "g": 185, "name": "rice, white, long-grain, raw"},
      {"line": 3, "fdc": 169655, "g": 20, "added_sugar": true, "name": "honey"}]}

- `servings`: the number of servings the recipe makes (from `servings`/`portions`).
- One item per food: `line` is the 0-based index of the ingredient line it comes from (a line with two foods
  gives two items; a line that is a heading, water, ice or "to serve" without an amount gives none).
- `fdc`: the closest SR Legacy food. Find it with `python3 nutrition/usda.py search <words>` (all words must
  appear in the name; try fewer or other words when nothing is found) and check it with
  `python3 nutrition/usda.py show <fdc>` (values per 100 g).
- `g`: grams of that food as it goes into the dish, for the whole recipe.

## Choosing the food
- Match the state: raw meat/vegetables -> the "raw" entry; dry pasta/rice/lentils -> "dry"/"raw"; an amount of
  cooked rice/pasta -> "cooked"; canned -> "canned" (drained solids if the line says drained).
- Match the salt: "low-sodium", "no salt added", "unsalted", "reduced sodium" -> pick that variant when it exists
  (canned beans/tomatoes, broth, butter, soy sauce, cheese). Ordinary canned foods and stock are salted.
- Broth/stock: "soup, stock, chicken, home-prepared" for homemade or low-sodium; "soup, chicken broth, ready-to-serve"
  for regular. Stock cubes: "soup, bouillon cubes and granules".
- Salt: "salt, table" (fdc 173468); a pinch = 0.4 g, 1/4 tsp = 1.5 g, 1 tsp = 6 g. "Salt to taste", "optional"
  without an amount -> leave out. Salt substitutes are potassium chloride: leave out and name them in `notes`.
- Sugar, honey, syrups, jam, date syrup, sweet sauces: set `"added_sugar": true`. Not fruit, milk or plain dried fruit.
- Cooking spray: 0.3 g oil per spray, "lightly coat" = 1 g. Oil "for frying": 1 tbsp (13.5 g) unless stated.
- Herbs and spices count (use the dried or fresh entry); a garnish without an amount -> 1 g.
- Brand or specialty products: the closest generic (e.g. "sugar substitute" -> sucralose-based sweetener, or leave out
  if it has no calories).

## Converting amounts to grams
- Use the gram weights USDA gives (`python3 nutrition/usda.py show` does not list portions, so use these):
  1 cup = 240 ml; 1 tbsp = 15 ml; 1 tsp = 5 ml. Water-like liquids 1 g/ml; oil 0.91 g/ml (1 tbsp = 13.6 g);
  flour 1 cup = 125 g; sugar 1 cup = 200 g; brown sugar packed 1 cup = 220 g; honey 1 tbsp = 21 g;
  butter 1 tbsp = 14 g; rice raw 1 cup = 185 g; cooked rice 1 cup = 158 g; oats 1 cup = 81 g; grated cheese
  1 cup = 100 g; chopped onion 1 cup = 160 g; chopped vegetables about 1 cup = 130-150 g; leafy greens 1 cup = 30 g;
  canned beans drained 1 cup = 170 g; milk 1 cup = 244 g; yogurt 1 cup = 245 g; egg large 50 g (white 33 g, yolk 17 g);
  garlic clove 3 g; medium onion 110 g; medium potato 170 g; medium tomato 123 g; medium carrot 61 g; medium apple 180 g;
  lemon juice of 1 lemon 45 g; chicken breast (one) 175 g raw unless stated.
- Use metric amounts when the line gives both.

## Rules
- Work blind: do not look at the recipe's published nutrition, the app data or the web. Only the input file and
  `nutrition/usda.py`.
- Every line with an amount gets an item, so nothing that carries potassium or phosphorus is missed.
- Add `"notes": "..."` to a calc file for anything uncertain (an unknown product, a missing amount you guessed).
- Check a few results with `python3 nutrition/usda.py calc <file>` (per-serving nutrients). If calories per serving
  look implausible for the dish, recheck weights.
