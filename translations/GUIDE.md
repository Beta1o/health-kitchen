# Recipe translation guide (English / Spanish / Arabic)

Readers are kidney patients (dialysis and CKD) and their families. Translate the way a professional medical-website translator would: accurate, natural and easy to follow while cooking. Never translate word for word, and never summarise.

## Input
`jobs_N.json` is a list of recipes. Each has `id`, `source_lang` (`en` or `es`), `translate_to` (a list of target languages), and the fields
`title`, `description`, `portions`, `serving_size`, `ingredients`, `steps`, `hints`, `food_choices`.

## Output
`out_N.json` is a JSON array with one object per input recipe, in the same order:
```json
{"id": 1687, "translations": {
  "es": {"title": "...", "description": "...", "portions": "...", "serving_size": "...",
         "ingredients": [[null, "..."]], "steps": [[null, "..."]], "hints": [[null, "..."]], "food_choices": ["..."]},
  "ar": { ...same keys... }
}}
```
- Produce exactly the languages in `translate_to`.
- `ingredients`, `steps` and `hints` are lists of `[group_label, text]` pairs. Keep the same number of items, in the same order. Translate the group label, or keep `null` if it is null.
- `food_choices` is a list of strings with the same count.
- `null` stays `null`. Never merge, split, drop or add items.

## All languages
- Keep every quantity, number, temperature, time and brand name exactly. Brand names stay in Latin script with their symbols (Knox®, Splenda®, Mrs. Dash®, DaVita, Kraft®).
- Don't add or remove health advice. Phrases like "low sodium", "unsalted" and "low-potassium" matter medically, so translate them precisely.
- Titles should sound like real recipe names in the target language. Keep well-known dish names (taco, quesadilla, paella, hummus, couscous) in their usual local spelling.
- Make "portions" and "serving_size" read naturally, e.g. "12 muffins" becomes "12 magdalenas" in Spanish and "12 كعكة مافن" in Arabic; "1 cup" becomes "1 taza" and "1 كوب".

## Spanish (es)
- Neutral Latin-American Spanish, using "usted" form in instructions ("Precaliente el horno...").
- Units: taza, cucharada, cucharadita, onza, libra, pizca, diente de ajo, lata, paquete.
- Food choice words: starch → almidón, fat → grasa, meat → carne, vegetable → verdura, fruit → fruta, milk → leche, high calorie → alto en calorías, low-potassium vegetable → verdura baja en potasio.

## English (en)
- Plain US English, matching DaVita's style ("Preheat oven to 350° F.").

## Arabic (ar)
- Clear Modern Standard Arabic in the imperative ("سخّن الفرن مسبقًا...").
- Western digits (1, 2, 3). Write fractions with Unicode characters: "1-1/2 cups" becomes "1½ كوب", "1/4 teaspoon" becomes "¼ ملعقة صغيرة". Use ½ ⅓ ⅔ ¼ ¾ ⅛; for any other fraction keep it as "3/16".
- Fahrenheit temperatures get a Celsius conversion rounded to the nearest 5: "400° F" becomes "400° فهرنهايت (200° مئوية)".
- Glossary:

| English | Arabic | English | Arabic |
|---|---|---|---|
| cup | كوب | tablespoon | ملعقة كبيرة |
| teaspoon | ملعقة صغيرة | ounce | أونصة |
| pound | رطل | pinch | رشة |
| clove (garlic) | فص | can | علبة |
| package | عبوة | slice | شريحة |
| low sodium | قليل الصوديوم | unsalted butter | زبدة غير مملحة |
| margarine | سمن نباتي (مارجرين) | non-dairy creamer | مبيض قهوة غير لبني |
| cream cheese | جبن كريمي | all-purpose flour | دقيق متعدد الاستخدامات |
| cornstarch | نشا الذرة | egg substitute | بديل البيض |
| bell pepper | فلفل رومي | zucchini | كوسا |
| cilantro | كزبرة خضراء | parsley | بقدونس |
| starch (food choice) | نشويات | fat (food choice) | دهون |
| meat (food choice) | لحوم | vegetable (food choice) | خضار |
| fruit (food choice) | فاكهة | milk (food choice) | حليب |
| high calorie | عالي السعرات | low-potassium vegetable | خضار منخفضة البوتاسيوم |
| medium-potassium fruit | فاكهة متوسطة البوتاسيوم | high-potassium vegetable | خضار عالية البوتاسيوم |
| dialysis | غسيل الكلى | kidney-friendly | مناسب لمرضى الكلى |

## Additional languages (ur, hi, fr, id, bn, tl)
Translate from the English text (`source_lang` is always `en` for these jobs). Use the same output format as above with the language code as the key, e.g. `{"id": 2430, "translations": {"ur": {...}}}`.

| Code | Language | Style |
|---|---|---|
| `ur` | Urdu | Clear standard Urdu in Nastaliq/Arabic script, polite آپ form ("اوون کو پہلے سے گرم کریں"). Western digits. Units: کپ، کھانے کا چمچ، چائے کا چمچ، گرام، ملی لیٹر. |
| `hi` | Hindi | Simple standard Hindi in Devanagari, polite आप form ("ओवन को पहले से गरम करें"). Western digits. Units: कप, बड़ा चम्मच, छोटा चम्मच, ग्राम, मिलीलीटर. |
| `fr` | French | Standard French, "vous" imperative ("Préchauffez le four"). Units: tasse, cuillère à soupe, cuillère à café, g, ml. |
| `id` | Indonesian | Standard Bahasa Indonesia, polite imperative ("Panaskan oven terlebih dahulu"). Units: cangkir, sendok makan, sendok teh, gram, ml. |
| `bn` | Bengali | Standard Bengali in Bengali script, polite আপনি form. Western digits. Units: কাপ, টেবিল চামচ, চা চামচ, গ্রাম, মিলি. |
| `tl` | Tagalog (Filipino) | Natural Filipino/Tagalog as used in recipes; common English cooking words may stay where Filipinos normally use them. Units: tasa, kutsara, kutsarita, gramo, ml. |

For all of these: keep every number and quantity exactly as in the English (unit names translated, values unchanged), keep brand names in Latin script, and translate medical words precisely (sodium, potassium, phosphorus, dialysis, kidney disease, diabetes).
