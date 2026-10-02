# Kidney Kitchen: DaVita recipe database and gallery

This project collects every kidney-friendly recipe published by DaVita (davita.com and espanol.davita.com) into a SQLite database. It removes recipes that are not halal, translates every recipe into English, Spanish and Arabic, and serves them through a searchable gallery.

| | |
|---|---|
| Recipes collected | 1,403 (1,258 English pages + 145 Spanish pages, matching the sites' sitemaps 1:1) |
| Removed as not halal | 187 (pork, pork-derived gelatin, alcohol), listed in `excluded_recipes` |
| Unique recipes in the gallery | 1,135 (81 Spanish pages are DaVita's own translations of English recipes and are merged with them) |
| Languages | English, Spanish, Arabic for every recipe. Official DaVita text where it exists, otherwise translated |

## Quick start: just open the gallery

Open `gallery/index.html` in any modern browser (Chrome, Edge, Firefox, Safari). Double-clicking it works, and no server is needed. Photos load from `gallery/thumbs/`.

To serve it on your network instead:

```bash
cd gallery
python3 -m http.server 8000
# then open http://localhost:8000
```

### What the gallery does

- **Search** recipe names and ingredients in the selected language. Arabic search ignores diacritics and alef/taa-marbuta variants.
- **Switch language** between English, Español and عربي at the top. Arabic switches the whole layout to right-to-left.
- **Refine results by** the same facets DaVita uses: Diet Type, Category, Dish Type, Cook Method, Holiday, Cuisine, Number of Servings and Includes a Recipe Photo. Counts update live as you filter.
- **Use kidney quick picks** (low sodium, low potassium, low phosphorus, under 300 calories, lower protein), **set nutrient limits** with per-serving sliders, and **leave out an ingredient** (e.g. "tomato, cheese").
- **Read colour-coded sodium, potassium and phosphorus values** on every card.
- **Open a recipe** for the image, portions, serving size, diet types, ingredients (tick them off), preparation (tap steps when done), nutrients per serving, kidney and kidney diabetic food choices, carbohydrate choices, helpful hints and the cooking video.
- **Save recipes**, which are kept in your browser. You can also **copy a recipe** as text and **link to one directly** (`index.html#r2430`).

## Setup to rebuild or refresh the data

Requirements: Python 3.10+ and internet access.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Pipeline

Run these in order from the project folder:

```bash
python3 scrape_davita.py     # 1. download recipes, ratings and images -> davita_recipes.db, images/
python3 halal_filter.py      # 2. remove pork / pork-derived gelatin / alcohol recipes (use --dry-run to review first)
python3 i18n.py build        # 3. link Spanish pages to their English originals, load official text per language
python3 i18n.py status       #    shows how many recipes still need a translation per language
python3 i18n.py export       # 4. (only if something is missing) write translation jobs to translations/jobs_N.json
#                                 translate them into translations/out_N.json following translations/GUIDE.md,
#                                 then check each batch: python3 translations/validate.py N
python3 i18n.py import       # 5. load translations into the database (never overwrites official DaVita text)
python3 build_gallery.py     # 6. regenerate gallery/
```

`scrape_davita.py` caches every API response and page in `cache/`, so later runs are fast. Delete `cache/` to force a fresh download. Flags: `--no-ratings` and `--no-images`.

## How the data was collected

- **Recipes, nutrients and categories** come from the sites' public WordPress REST API (`/wp-json/wp/v2/dv-recipe` and its taxonomies). robots.txt allows crawling.
- **Star ratings** come from each recipe page's header, since the API doesn't include them. The Spanish site shows no ratings.
- **Completeness check:** the database URLs match `dv-recipe-sitemap*.xml` on both sites exactly (1,403 = 1,403), and the English search page itself reports "1258 results found".
- **Not included:** the 51 DaVita cookbooks, which are downloads behind a DaVita account sign-in.

## Halal filter

`halal_filter.py` checks every ingredient line (English and Spanish), plus titles for unambiguous pork words. It removes recipes containing:

| Reason | Examples | Recipes removed |
|---|---|---|
| Pork | pork, bacon, ham, prosciutto, Andouille/pork sausage, chorizo (pork), carnitas, baby back ribs, cerdo, jamón | 79 |
| Pork-derived gelatin | gelatin, Jell-O gelatin, Knox® gelatin, marshmallows, gelatina, malvaviscos | 55 |
| Alcohol | wine, cooking wine, sherry, Marsala, beer, rum, brandy, champagne, mirin, Shaoxing wine, vino, jerez | 59 |

Some recipes match more than one reason, so the 187 total is lower than the sum.

Kept, as permissible under the mainstream view: wine vinegar, root beer, marshmallow crème/fluff (no gelatin), turkey bacon, turkey/chicken/beef sausage, and the beef-based "Easy Chorizo". Three kept recipes use **rum or root beer extract** as a flavouring (Vanilla Root Beer Delight, Spiced Eggnog, Zingy Spiced Pears; `SELECT * FROM ingredients WHERE text LIKE '%extract%' AND (text LIKE '%rum%' OR text LIKE '%root beer%')`). Remove them too if you follow the stricter view.

Every removed recipe is kept for review in the `excluded_recipes` table with its reason and the exact ingredient lines that matched.

## Database (`davita_recipes.db`)

| Table | Contents |
|---|---|
| `recipes` | One row per source page: title, url, category, portions, serving size, rating, comments, the 11 nutrients (number columns plus `_raw` text), carbohydrate choices, image url/path, video url/poster/subtitles, raw HTML. `canonical_id` points Spanish translations at their English recipe |
| `ingredients`, `steps`, `hints`, `food_choices` | Ordered lists per page as scraped, with sub-group labels (e.g. "Dressing") |
| `terms`, `recipe_terms` | Diet type, category, dish type, cuisine, holiday, cooking method |
| `recipe_i18n`, `ingredients_i18n`, `steps_i18n`, `hints_i18n`, `food_choices_i18n` | Text per canonical recipe and language (`en`/`es`/`ar`). `source` is `davita` (official) or `translated` |
| `excluded_recipes` | Recipes removed by the halal filter, with reasons |
| `recipe_overview` (view) | One row per page with diet types and nutrients |

Example queries:

```sql
-- Arabic version of a recipe
SELECT title, portions, serving_size FROM recipe_i18n WHERE recipe_id = 2430 AND lang = 'ar';
SELECT text FROM ingredients_i18n WHERE recipe_id = 2430 AND lang = 'ar' ORDER BY position;

-- low sodium, low potassium dialysis recipes
SELECT title, sodium_mg, potassium_mg FROM recipe_overview
WHERE diet_types LIKE '%Dialysis%' AND sodium_mg <= 140 AND potassium_mg <= 200;
```

## Project files

| File | Purpose |
|---|---|
| `scrape_davita.py` | Downloads everything into the database |
| `halal_filter.py` | Removes non-halal recipes and records why |
| `i18n.py` | Multilingual tables, translation export/import, coverage status |
| `terms_i18n.py` | Filter values (categories, diets, ...) in English, Spanish and Arabic |
| `translations/` | Translation guide, jobs, translated output and validator |
| `build_gallery.py`, `gallery_template.html` | Builds the gallery |
| `gallery/` | The built app (`index.html`, thumbnails, packed image chunks, `artifact.html` for publishing) |
| `images/` | Full-size recipe photos |
| `cache/` | Raw API responses (safe to delete) |

## Notes

- The colour levels in the gallery (sodium, potassium and phosphorus per serving) are a sorting aid only. Patients should follow the limits their dietitian gives them.
- Recipe content and photos belong to DaVita Inc. This project is for personal and educational use.
