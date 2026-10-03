# Excluded-ingredient text review (v2)

The app never shows pork or pork products (bacon, ham, lard, chorizo/salami/pepperoni unless clearly turkey/beef/chicken), pork-derived gelatin (gelatin, Jell-O, marshmallows; agar is fine) or alcohol (wine, beer, rum, sherry, mirin, sake, liqueur, cooking wine, champagne...). Vinegars (red/white wine vinegar, rice wine vinegar, sherry vinegar), turkey bacon, beef bacon, turkey ham, root beer, ginger beer, non-alcoholic drinks, vanilla/rum extract, "sour cream" (Urdu سور کریم), vine tomatoes (Hindi वाइन टमाटर), Winesap apples and grapes (Indonesian anggur merah/hijau as fruit) are FINE.
Never mention religion or the word "halal" in any rewrite.

Each item in in_N.json is one text (recipe_id, field = title|description|ingredients|steps|hints, position, text per matching language, key).
Decide per item:
- "keep": false match (the text is fine).
- "rewrite": the text mentions an excluded item only as an option, swap, pairing or story (e.g. "works with beef or pork", "serve with roast pork", "traditionally cooked with lard", "add bacon if you like", "wine (or lemon juice)"). Rewrite minimally so the excluded item disappears and the sentence still reads naturally ("works with beef", "lemon juice", "traditionally cooked with a lot of fat"). If a hint/step is ONLY about the excluded item, use null to delete it (hints and steps only; never null a title/description/ingredient).
- "exclude": the recipe really USES an excluded item as an ingredient or a step needs it (e.g. ingredient "4 slices bacon", step "add the wine" with wine in the ingredients). The whole recipe will be removed.

IMPORTANT: the same text exists in up to 9 languages (en, es, ar, ur, hi, fr, id, bn, tl). For "rewrite", produce the new text for EVERY language of that recipe/field/position that still mentions the item — read them with:
  python3 -c "import sqlite3,sys;d=sqlite3.connect('davita_recipes.db');rid,f,p=int(sys.argv[1]),sys.argv[2],int(sys.argv[3]);q=('SELECT lang,'+f+' FROM recipe_i18n WHERE recipe_id=?',(rid,)) if f in('title','description') else ('SELECT lang,text FROM '+f+'_i18n WHERE recipe_id=? AND position=?',(rid,p));[print(l,'|',t) for l,t in d.execute(*q)]" RID FIELD POS
and return a map {lang: new text or null} with only the languages you change, and the ORIGINAL texts of those languages in "orig" (exact copy, used as a guard).
Output translations/policy_v2/out_N.json: [{"key": K, "recipe_id": R, "field": F, "position": P, "action": "keep|rewrite|exclude", "orig": {lang: original}, "text": {lang: new|null}, "reason": "short"}] — one entry per input item, same order.
