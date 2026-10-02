# External recipe source format

Each source scraper writes `sources/<key>/recipes.json` (a JSON array, UTF-8) and downloads photos to `sources/<key>/images/`. `<key>` is one of `davita_sa`, `kidneycareuk`, `aakp` or `myrenalnutrition`. The main pipeline (`import_sources.py`) loads these files into `davita_recipes.db`. It also applies the halal filter and creates the translation jobs, so scrapers must **not** filter or translate anything themselves.

## Rules for scrapers
- Respect robots.txt. Use a normal browser User-Agent, 1 to 4 concurrent requests, retry 429/5xx with backoff, and cache raw pages under `sources/<key>/cache/` so reruns don't refetch.
- Never get around logins, paywalls, CAPTCHAs or bot protection. If a page is blocked, skip it and list it in `sources/<key>/skipped.json`.
- Collect **every** recipe the source publishes. Then check the count against the source's own listing, sitemap or index, and report both numbers.
- Write the scraper as `sources/<key>/scrape.py` (Python 3, `requests` plus the standard library only; `html.parser`/regex, since BeautifulSoup is not installed). It must be re-runnable.

## Recipe object
```json
{
  "source": "kidneycareuk",                  // the <key>
  "source_name": "Kidney Care UK",           // display name
  "source_id": "slug-or-id",                 // stable and unique within the source
  "url": "https://...",                      // canonical recipe page
  "lang": "en",                              // language of this text: en | ar | es
  "title": "...",
  "description": "..." ,                     // short intro, or null
  "image_url": "https://...",                // full-size photo, or null
  "image_path": "sources/kidneycareuk/images/<source_id>.jpg",  // downloaded copy, or null
  "portions": "4",                           // as written ("4", "12 muffins"), or null
  "serving_size": "1 cup",                   // or null
  "category": "Chicken & Turkey",            // best fit among the 14 below, never null
  "diet": ["Dialysis"],                      // only diet types the source states (values below)
  "dish": [], "cuisine": [], "method": [],   // optional; use the English values below where they fit
  "nutrients": {                             // per serving; null when not given; numbers only
    "calories": 228, "protein_g": 3, "carbohydrates_g": 31, "fat_g": 10, "cholesterol_mg": 31,
    "sodium_mg": 118, "potassium_mg": 48, "phosphorus_mg": 35, "calcium_mg": 12, "fiber_g": 1.0,
    "added_sugar_g": 17
  },
  "nutrients_raw": "original nutrition text, if any",
  "ingredients": [[null, "1 cup sugar"], ["For the sauce", "2 tbsp oil"]],  // [group label or null, text]
  "steps": [[null, "Preheat oven..."]],
  "hints": [[null, "Tip text..."]],          // tips, notes, dietitian advice, swaps
  "food_choices": [],                        // e.g. "1 starch", if the source lists exchanges
  "carb_choices": null,
  "video_url": null,
  "prep_time": null, "cook_time": null, "total_time": null,
  "translation_of": null                     // for a second-language copy of the same recipe: the source_id of the primary-language record
}
```

Convert units to these columns: kcal to calories, and g or mg as named. If a source gives mmol, convert: sodium mmol × 23 = mg, potassium mmol × 39.1 = mg, phosphate mmol × 31 = mg. If a source gives nutrients per 100 g or per whole recipe only, convert them to per serving when the portion count is known. Otherwise leave the nutrients null and keep the text in `nutrients_raw`.

### Categories (exactly these strings)
Appetizers & Snacks · Beef, Lamb & Pork · Beverages · Breads · Breakfast & Brunch · Chicken & Turkey · Desserts · Fish & Seafood · Pasta, Rice & Grains · Pizza & Sandwiches · Salads & Dressings · Sauces & Seasonings · Soups & Stews · Vegetables

### Diet values
CKD non-dialysis · Diabetes · Dialysis · Gluten-free · Heart Healthy · Higher Potassium · Lower Potassium · Lower Protein · Vegetarian

### Dish / method / cuisine values (use these when they fit, otherwise omit)
dish: 5 or less ingredients, Bread, Budget, Cake, Candy, Cookies, Easy, Freezer, Meatless Entree, Muffin, One-Dish Meal, Picnic, Pie, Potluck, Quick, Refrigerator, Soup, Stew, Stir-fry
method: Bake, Fry, Grill, Microwave, No Cooking, Oven, Roast, Slow Cooker, Stove Top
cuisine: American, Asian, Caribbean, Chinese, Filipino, French, German, Greek, Hawaiian, Indian, Irish, Italian, Japanese, Jewish, Mediterranean, Mexican, Middle Eastern, Native American, South American, Southern

## Report
Finish with `sources/<key>/report.json`, in this form: `{"listed": N, "scraped": N, "with_image": N, "with_nutrients": N, "skipped": N, "notes": "..."}`.
