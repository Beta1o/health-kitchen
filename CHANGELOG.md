# Changelog

All notable changes to Health Kitchen. Dates are YYYY-MM-DD.

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
