<p align="center">
  <a href="https://beta1o.github.io/health-kitchen/"><img src="assets/logo.svg" width="96" height="96" alt="Health Kitchen logo"></a>
</p>

<h1 align="center">Health Kitchen</h1>

<p align="center">
  Recipes for kidney disease, diabetes, high blood pressure and heart health,<br>
  in <b>English</b>, <b>Español</b>, <b>العربية</b> and six more languages, with nutrition plans built in.<br><br>
  <a href="https://beta1o.github.io/health-kitchen/"><b>Open the app →</b></a>
</p>

---

## What's inside

| | |
|---|---|
| Recipes in the app | **3,310** unique recipes |
| Sources | DaVita (davita.com, espanol.davita.com, davita.sa), AAKP, Kidney Care UK, My Renal Nutrition, Diabetes Food Hub (ADA), Diabetes UK |
| Languages | English, Spanish and Arabic for every recipe; Urdu, Hindi, French, Indonesian, Bengali and Tagalog being completed (a recipe appears in a language once its full translation is in). Official text is used where the source publishes it; the rest is translated |
| Photos | 2,609 recipes. Recipes without one get a colour-coded illustrated title card |
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

## Accounts (local server with PostgreSQL)

The app also runs with real accounts on a local server. Users sign up with email and password and keep their profile, health plan, weight log, My day, saved recipes and settings in a PostgreSQL database. An admin page lists users and manages roles.

```bash
# one-time setup (no sudo needed): a PostgreSQL cluster owned by you on port 5440
/usr/lib/postgresql/16/bin/initdb -D ~/.local/share/health-kitchen/pgdata -U hk_owner --auth=scram-sha-256 --pwprompt
/usr/lib/postgresql/16/bin/pg_ctl -D ~/.local/share/health-kitchen/pgdata -o "-p 5440 -k /tmp" -l ~/.local/share/health-kitchen/pg.log start
psql -h 127.0.0.1 -p 5440 -U hk_owner -d postgres -c "CREATE DATABASE health_kitchen"
psql -h 127.0.0.1 -p 5440 -U hk_owner -d health_kitchen -f server/schema.sql
psql -h 127.0.0.1 -p 5440 -U hk_owner -d health_kitchen -c "ALTER ROLE hk_api PASSWORD 'choose-a-password'"
python3 -m venv ~/.venvs/hk && ~/.venvs/hk/bin/pip install "psycopg[binary]" psycopg_pool fastapi uvicorn

# run (starts PostgreSQL if needed, then the server)
HK_DB_URL=postgresql://hk_api:choose-a-password@127.0.0.1:5440/health_kitchen server/run.sh
# open http://localhost:8099  (one port: the app, accounts, admin and API)
```

- **The first account you create becomes the admin.** Admins can promote other users or remove accounts from the Admin page (Account → Admin).
- **Security:** passwords are hashed with scrypt, and sessions are random tokens stored hashed with a 30-day expiry. The API connects as `hk_api`, a role with no superuser rights and no `BYPASSRLS`. Every request sets the signed-in user, and PostgreSQL **row-level security** (`server/schema.sql`) lets each user read and write only their own rows. Admins can read all of them.
- **Without the server:** the GitHub Pages version and opening `gallery/index.html` directly both work without accounts, keeping data on the device only.
- **Outside this computer:** to reach the server from other devices, put it behind HTTPS (for example a reverse proxy) before sharing it.

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

The repository stores it compressed (GitHub limits files to 100 MB). Unpack it before running any script:

```bash
gunzip -k davita_recipes.db.gz
```

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

Recipe text, nutrition data and photos belong to their publishers: DaVita Inc., the American Association of Kidney Patients, Kidney Care UK, My Renal Nutrition (Vitaflo), the American Diabetes Association (Diabetes Food Hub) and Diabetes UK. Every recipe links back to its original page. The project code is provided as-is for personal and educational use.
