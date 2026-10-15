# Changelog

All notable changes to Health Kitchen. Dates are YYYY-MM-DD.

## [Unreleased]
### Open
- Owner decisions: full GI database search public or admin-only until the University of Sydney replies; keep or reword the "without it / with half" numbers; staging before release. Details and owner tasks in CHATLOG.md, "Pick up here".

## [0.9.0] - 2026-10-15
Every recipe now has a cuisine, diet types and almost all a cooking method; more glycemic loads and dish types.
### Added
- Glycemic load for 3,286 recipes (was 2,897), the 70% evidence rule unchanged:
  - Ingredient lines whose amount the parser cannot read ("1 x 400g tin chickpeas", "4 x flour tortillas") take their grams from the recipe's USDA calculation (`glycemic.weights_for`).
  - Up to 10 g of available carbohydrate a serving, the load is low whatever the GI, so it is shown as a ceiling ("≤ 8") when the GI is not known (was up to 5 g).
- Dish types from each recipe's own text and times, the same rules for every source (`dish_tags.py`): 5 or less ingredients, Quick (30 minutes or less), Soup, Stew, Cake, Muffin, Cookies, Bread, Pie, Stir-fry, Meatless Entree. Each rule was checked against the DaVita and ADA tags (Soup 90%, Stew 91%, Muffin 97%, 5 or less ingredients 96% of their tagged recipes found). Budget, Easy, Potluck, Picnic, Freezer, Refrigerator, One-Dish Meal and Candy are judgement calls and are not derived.
- Vegetarian from the ingredients and title (no meat, poultry, fish or seafood, meat stock, gelatin or marshmallows; "chicken or vegetable broth" counts as chicken): 762 more recipes. Gluten-free is not derived (hidden gluten).
- Cuisine for the 474 recipes without one (`translations/cuisine_fill.json`; named dishes get their cuisine, the rest International) and cooking method for 173 more (`translations/method_fill.json`).
### Tested and not used
- A second blind USDA calculation for the 442 recipes whose first one did not match: the retries that passed were less accurate (potassium within 30% for 63% against 83%), so they were dropped and those recipes keep no estimate.
### Still empty (on purpose)
- Glycemic load for 579 recipes (too little of the carbohydrate has a measured GI); potassium for 288 and phosphorus for 441 recipes (no calculation matched the published numbers, or the publisher labels them lower in potassium); cooking method for 20 single cooked items; dish type for 622 recipes that match none of the objective rules; Heart Healthy is not derived (saturated fat is not published).

## [0.8.0] - 2026-10-15
Diet types and nutrients filled for every recipe the numbers allow.
### Added
- Missing potassium, phosphorus, calcium, cholesterol and added sugar estimated from the ingredient list (USDA SR Legacy, `nutrition/estimate/`) for 1,902 recipes. An estimate is used only when the calculation reproduces the publisher's calories and protein or carbohydrate within 25% (or does after scaling by one consistent factor, when the serving count differs: 210 recipes). It never replaces a published number and is marked "≈" with a note in the nutrition table (9 languages).
  - Checked blind against published values: potassium on 1,029 ADA recipes, 83% within 30%, median +2%; potassium and phosphorus on 120 DaVita/AAKP recipes, 89% and 88% within 30%, median 0%. With the 15% margin, no DaVita/AAKP recipe was wrongly put under the CKD/dialysis phosphorus or potassium limits (2% of ADA recipes for potassium).
  - No potassium estimate for recipes with salt substitutes or sodium-free stock (potassium chloride), or ones the publisher labels lower in potassium (kidney publishers count leaching, which raw USDA values do not). Nutrients USDA lacks for more than 10% of the recipe's weight are not estimated.
- Diet-type tags from each recipe's own nutrition, with the same rules for every source (`diet_tags.py`): Lower/Higher Potassium, Lower Protein, CKD non-dialysis, Dialysis, Diabetes. CKD and dialysis limits were set against the tags DaVita and AAKP dietitians gave their recipes (83% and 94% agreement). Estimated values must clear a limit by 15%. Publisher tags are kept; those the published numbers contradict are listed in `diet_tags_report.json` for a dietitian.
- Cooking method read from the steps for 1,089 recipes whose publisher gives none.
### Changed
- Kidney meal plans: a "Lower Protein" tag alone qualifies a recipe for CKD menus only when potassium and phosphorus are known and within the CKD limits.
- Recipes with known potassium and phosphorus: 1,532 → 3,386 of 3,865. "Heart Healthy" stays a publisher tag (no numeric rule reproduced it; the Heart-healthy quick pick filters by the numbers).
### Not filled (on purpose)
- 479 recipes still lack potassium or phosphorus: their calculation did not match the published numbers (Diabetes UK 174, ADA 192 phosphorus only, This Healthy Kitchen 58, Kidney Care UK 48 potassium, others 7).
- Cuisine (474 recipes) and dish type are not guessed; GL stays empty for 968 recipes under the 70% rule.

## [0.7.0] - 2026-10-10
Safety review (an "LLM council" of five independent reviews, peer review and a chairman's verdict).
### Changed
- Kidney plans: CKD and CKD-with-diabetes menus keep within the protein limit (dialysis keeps protein as a goal); no weight-loss calorie cut and no weight timeline with kidney disease (plan it with the nephrologist or renal dietitian); kidney-safe blood sugar tips instead of "beans, lentils, whole grains".
- Diet plan asks about diabetes medicines. With insulin or sulfonylureas it shows a low blood sugar warning, has no free day or free meal, and keeps calories at maintenance unless the doctor approved a cut. "This is a guide. Show this plan to your doctor or dietitian." is printed at the top.
- Glycemic estimates are shown only when the matched ingredients (plus non-starchy vegetables) explain at least 70% of the published carbohydrate (2,897 recipes); no hidden default GI; low-carbohydrate dishes without a GI show GL as a ceiling; each panel says how much of the carbohydrate the GI is based on.
- The blood sugar panel leads with carbohydrate per serving, and shows it even when there is no GI estimate.
### Added
- tests/gi_regression.py: 20 fixed recipes whose carbohydrate, potassium, GI and GL must not change by accident; the build stops if they do.
- tests/smoke.js: browser checks in English, Arabic and Spanish, plus diet plan safety rules for CKD, CKD with diabetes, dialysis and insulin.

## [0.6.0] - 2026-10-10
### Added
- Glycemic index and glycemic load: an estimated GI and GL per serving for 3,281 recipes, worked out from the ingredients with values from the University of Sydney GI database (glycemicindex.com; foods with pork, gelatin or alcohol left out).
- A "Blood sugar impact" panel on each recipe: GI and GL with low/medium/high bands, GL for my portion, the ingredients that raise blood sugar most with their share of the sugar load, and a tip when the load is high.
- Ingredient lines that carry the sugar load are marked with their GI, in every language.
- A glycemic load filter (low, medium, high) and a "Lowest glycemic load" sort.
- With a diabetes plan: the GL on recipe cards, a GL note in the dietitian's view and the day's glycemic load in My day.
- Glycemic index is a module in the admin's access table, so it can be turned on or off per role (admin, supervisor, user, visitor).
- My diet plan: a menu for the whole journey, one week per stage, each sized to the calories for the weight in that stage, placed after the main information.
- My diet plan: a blood sugar section (daily glycemic load of the menu, GI and GL bands, tips) and the GL of every menu item and day.
- My diet plan: a free day (or, with diabetes or kidney disease, a free meal) on a chosen weekday, with when and how much; the most active day is suggested.
- Meal plans pick recipes made for the plan's condition (diabetes, dialysis, CKD); diabetes plans leave out high glycemic load recipes.
- Body figures follow the sex: a woman with long hair and a dress, a man with short hair and broader shoulders.
- Account overview: glycemic load today and the 7-day average.
- Admins can give any role, including admin, to other users (listed admin emails always stay admin).
- Account: a Glycemic index tab with today's glycemic load from My day, the last 14 days, about 50 foods by GI (from the University of Sydney data) linked to the recipes whose ingredients use them, and low glycemic load recipes for the plan.
- My diet plan: choose one or more cuisines for the menus; on the free day the planned meals are replaced (a free meal replaces dinner).
- Glycemic index tab: search the whole University of Sydney GI database (4,361 foods, values as published, pork, gelatin and alcohol foods left out) by name, category, country, GI and GL band, serving size and carbohydrate per serving; loaded only when the tab opens.
- Combined GI of a whole meal or day (carbohydrate-weighted) in My day, the diet plan menus and the Glycemic index tab; the recipe panel explains the GI is of the whole dish.
- For each ingredient that raises blood sugar: what leaving it out, or using half, would do to the dish's GI and GL.
- GI database search: food names in all 9 languages (translations/gi_names), countries in the reader's language, each food linked to the app's ingredient group and the recipes that use it, and a filter for foods used in the recipes.
- Standard categories shared by recipes and the GI database: the recipe categories plus Fruit, Legumes, Dairy, Nuts & Seeds, Sugars & Sweeteners, Traditional Dishes, Special Nutrition and Other, in every language.
- All new text in 9 languages.

### Fixed
- Printed diet plan: the food lists no longer overlap the menu; Arabic shows ranges, fractions (1½) and arrows in the right order, "at most" in words instead of a mirrored ≤, Arabic units, and weight and BMI on separate lines.
- Removed the supervisor note under the role buttons.
- Exercise plan: walking and cycling add up exactly to the weekly minutes, with a total row that matches the calories burned.
- The access table showed "undefined" for the My diet plan module.
- The Supabase connection details on the admin page are masked until "Show" is pressed.

## [0.5.0] - 2026-10-03
### Added
- Saudi kitchen: over 120 home dishes (kabsa, mandi, jareesh, marqooq, qursan, saleeq, kleeja and more) written from the encyclopediacooking.com Saudi listing, each checked against at least two other sources, made healthier (less salt and fat, no stock cubes, lean meat, measured rice) with nutrition computed from USDA data and a "Suitable for" line.
- This Healthy Kitchen recipes (433).
- Community recipes: signed-in users share recipes with structured amounts and metric units; nothing is published until an admin approves it.
- Account page with tabs (overview with statistics and charts, my information with the health plan, health and goals, food preferences with ingredient suggestions, weight log, my recipes, settings).
- Admin page: user search, details, password reset, disable or enable accounts, CSV export, sign-up statistics, recipe review.
- Meal plans can be limited to one or more cuisines. A "No plan" option shows all recipes.

### Changed
- Only the configured admin email can be an admin; everyone else is a user (enforced in the database).
- Settings live in My account only; the Arabic form of address follows the sex in My information.
- Categories are ordered by meal, and 321 external recipes were moved to the right category.
- Cuisines: one "American"; "Middle Eastern" split into country cuisines.
- Recipe cards are the same height; source tags only appear on the recipe page.

### Fixed
- Texts that still mentioned excluded ingredients (in any language) are rewritten or the recipe is removed (`policy_scan.py`).

## [0.4.0] - 2026-10-03
### Added
- Diabetes Food Hub (ADA) and Diabetes UK recipes: 3,310 unique recipes in total.
- Accounts on a local server (`server/`): sign up with email and password, with profile, health plan, weight log, My day, saved recipes and settings stored in PostgreSQL. Row-level security limits each user to their own rows; admins get an Admin page for users and roles.
- Dashboard with condition switcher, daily targets, recommended meals sized to your targets, tips, calculators and a weight tracker.
- Interface in Urdu, Hindi, French, Indonesian, Bengali and Tagalog. A recipe appears in a language only once its full translation is in, so text never mixes languages.
- Feminine forms of address for Arabic instructions ("Speak to me as").
- About page with sources and latest updates.

### Changed
- English, Spanish and Arabic now cover every recipe (3,310 each).
- The language picker is in Settings only; the header no longer has one.
- My information (profile, goals, foods to avoid, doctor's notes) moved from Settings to the Account page.
- Settings sections are collapsible.
- Gallery build is much faster (added database indexes).

### Fixed
- Hidden overlays (such as the sign-in screen) could stay visible because their display style overrode `hidden`.
- Links like `#ar-dash` now open in the right language.

## [0.3.0] - 2026-10-02
### Added
- External sources: AAKP (198 recipes), Kidney Care UK (48), My Renal Nutrition (82) and DaVita Saudi Arabia (8 new recipes plus photos for 5 DaVita recipes), stored in a shared format (`sources/FORMAT.md`) and loaded by `import_sources.py`.
- A Source filter, source badges on cards, and an original-source link on every recipe.
- Phone layout: compact header, bottom navigation (Home, Filters, Meal plans, My day, Saved) and a one-row recipe toolbar.
- Light and dark themes with a toggle (system, dark, light), applied before first paint.
- Logo and favicon. The logo links back to the home view.
- PDF export of a recipe, with a print layout.
- `CHANGELOG.md` and `CHATLOG.md`.

### Changed
- Recipes open as an in-app page instead of a pop-up, and browser Back/Forward work.
- Recipe photos use sharp 1280px copies shown at their natural shape, so they are no longer stretched.
- Cards and the hero legend show the active plan's key nutrients instead of always sodium, potassium and phosphorus.
- Fonts are embedded in the page, so it loads with no layout shift and no requests to Google Fonts.
- Neutral wording for the ingredient policy (`ingredient_filter.py`). Religious wording was removed from the app and the docs.

### Fixed
- The filter drawer on phones opened only a dark overlay when used from a recipe page.
- Translated recipes credited DaVita even when they came from another source.
- The plan summary in Arabic mixed text and numbers in the wrong order.

## [0.2.0] - 2026-10-02
### Added
- Rebranded as **Health Kitchen**: covers kidney disease, diabetes, high blood pressure and heart health.
- Health plans (kidney: dialysis / CKD / CKD with diabetes, diabetes, high blood pressure, heart health, general eating), each with editable limits and goals.
- A dietitian's view on each recipe: meters against the plan, the phosphorus-to-protein ratio and automatic notes.
- My day planner with daily rings, and meal plans for 7, 14, 30, 60, 120 or 365 days.
- An animated hero with a featured carousel, staggered cards, a heart burst on save and a celebration when all steps are done.
- Filter sections matching DaVita's (Diet type, Category, Dish type, Cook method, Cuisine, Number of servings, Includes a photo) with live counts.
- English, Spanish and Arabic for every recipe, with a right-to-left Arabic layout.

### Removed
- Star ratings, review counts and the occasions/holiday filter.

## [0.1.0] - 2026-10-02
### Added
- A scraper for all 1,258 davita.com and 145 espanol.davita.com recipes through the public WordPress API, into SQLite (`davita_recipes.db`).
- An ingredient policy that removes recipes with pork, pork-derived gelatin or alcohol, recording each removal and its reason.
- The first static recipe gallery with search, filters and the recipe view.
- The README, `requirements.txt` and translation guide.
