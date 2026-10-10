# Changelog

All notable changes to Health Kitchen. Dates are YYYY-MM-DD.

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
