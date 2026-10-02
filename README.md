<p align="center">
  <a href="https://beta1o.github.io/health-kitchen/"><img src="assets/logo.svg" width="96" height="96" alt="Health Kitchen logo"></a>
</p>

<h1 align="center">Health Kitchen</h1>

<p align="center">
  Recipes for kidney disease, diabetes, high blood pressure and heart health,<br>
  in <b>English</b>, <b>Español</b> and <b>العربية</b>, with nutrition plans built in.<br><br>
  <a href="https://beta1o.github.io/health-kitchen/"><b>Open the app →</b></a>
</p>

---

## What's inside

| | |
|---|---|
| Recipes in the app | **1,469** unique recipes |
| Sources | DaVita (davita.com, espanol.davita.com, davita.sa), AAKP, Kidney Care UK, My Renal Nutrition |
| Languages | English, Spanish and Arabic for every recipe. Official text is used where the source publishes it; the rest is translated |
| Photos | 774 recipes. Recipes without one get a colour-coded illustrated title card |
| Nutrition | Calories, protein, carbohydrates, fat, cholesterol, sodium, potassium, phosphorus, calcium, fiber and added sugar per serving |

## The app

Open `gallery/index.html` in any modern browser, or use the hosted version at **https://beta1o.github.io/health-kitchen/**. It works offline: data, fonts and images all ship with the page.

- **Health plans:** kidney (dialysis, CKD, CKD with diabetes), diabetes, high blood pressure (DASH), heart health and general eating. Each plan tracks the nutrients that matter for it, as limits or goals, using values you can edit.
- **Recipe cards** show the active plan's key nutrients, coloured by their share of one meal.
- **Dietitian's view** on each recipe: meters against your plan, the phosphorus-to-protein ratio for kidney plans, and automatic notes.
- **My day:** add recipes to today's plan and watch the daily rings fill.
- **Meal plans** for 7, 14, 30, 60, 120 or 365 days, built from the collection to stay within your daily limits.
- **Search and filters:** search in any language, filter by diet type, category, dish type, cook method, cuisine, number of servings, photo and source, set nutrient limits, or leave out an ingredient.
- **Cooking aids:** tick off ingredients and steps, save favourites, copy a recipe, export it to PDF, or share a link to it (`#en-r2430`, `#ar-r2430`).
- **Light and dark themes**, a right-to-left layout for Arabic, and bottom navigation on phones.

Nutrition levels and plan amounts are a guide only. Patients should follow the limits their doctor or dietitian gives them.

## Ingredient policy

Recipes containing pork or pork products, pork-derived gelatin (gelatin, Jell-O, marshmallows) or alcohol (wine, beer, spirits, mirin, cooking wine) are left out. That is **219** recipes: 100 pork, 58 gelatin and 70 alcohol, where a recipe can have more than one reason. Each one is recorded with the exact matching ingredient lines in the `excluded_recipes` table.

Wine vinegar, root beer and marshmallow crème are kept. Hints and descriptions that suggested pork or alcohol as a swap or serving idea were rewritten in all three languages (`translations/policy_text_fixes*.json`).

## Rebuild the data

Requirements: Python 3.10+, internet access and `pip install -r requirements.txt` (requests, Pillow).

```bash
python3 scrape_davita.py            # 1. DaVita recipes, ratings, photos      -> davita_recipes.db (recreates base tables)
python3 sources/<key>/scrape.py     # 2. each external source                  -> sources/<key>/recipes.json
python3 import_sources.py           # 3. load external sources into the database
python3 ingredient_filter.py        # 4. apply the ingredient policy (--dry-run to review)
python3 i18n.py build               # 5. link translations, load official text per language
python3 i18n.py import              # 6. load translations/out_*.json
python3 i18n.py fixes               # 7. apply text policy fixes (safe to repeat)
python3 i18n.py status              #    coverage per language
python3 fonts/fetch_fonts.py        # 8. (once) embed the app fonts
python3 build_gallery.py            # 9. build gallery/
```

The steps must run in this order, because each one builds on the previous. To translate recipes that are still missing a language, run `python3 i18n.py export`, translate the new `translations/jobs_*.json` files following `translations/GUIDE.md`, check them with `translations/validate.py` and `translations/crosscheck.py`, then repeat steps 6, 7 and 9.

Raw downloads (`cache/`, `images/`, `sources/*/cache`, `sources/*/images`) are not in the repository; the scrapers recreate them.

## Database: `davita_recipes.db` (SQLite)

| Table | Contents |
|---|---|
| `recipes` | One row per source page: site, source name, language, URL, category, portions, serving size, 11 nutrients (number and raw text), carbohydrate choices, image, video, times. `canonical_id` links translations of the same recipe |
| `ingredients`, `steps`, `hints`, `food_choices` | Text per page, as published |
| `recipe_i18n`, `*_i18n` | Text per recipe and language (`en`/`es`/`ar`). `source` is `davita` for official text and `translated` otherwise |
| `terms`, `recipe_terms` | Diet type, category, dish type, cuisine, holiday, cooking method |
| `excluded_recipes` | Recipes left out by the ingredient policy, with the reason |

```sql
SELECT title, portions FROM recipe_i18n WHERE recipe_id = 2430 AND lang = 'ar';
SELECT text FROM ingredients_i18n WHERE recipe_id = 2430 AND lang = 'es' ORDER BY position;
```

## Not included

- **Mayo Clinic** blocks automated access.
- **DaVita cookbooks** are behind a sign-in.
- The **davita.sa cookbook PDFs** are not parsed.
- **AAKP:** 4 listed recipes link to the wrong PDF on AAKP's own site.

## Credits

Recipe text, nutrition data and photos belong to their publishers: DaVita Inc., the American Association of Kidney Patients, Kidney Care UK and My Renal Nutrition (Vitaflo). Every recipe links back to its original page. The project code is provided as-is for personal and educational use.
