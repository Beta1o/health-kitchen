#!/usr/bin/env python3
"""Multilingual recipe text (English, Spanish, Arabic).

Every recipe shown in the gallery is a "canonical" recipe: an English DaVita
page, or a Spanish page that has no English original. Spanish pages that are
DaVita's own translation of an English page (same nutrient values) are linked
to that English recipe and supply its official Spanish text.

Text for each canonical recipe and language lives in the *_i18n tables, with
`source` = 'davita' (official text from the site) or 'translated'.

Usage:
  python3 i18n.py build     # (re)create i18n tables from the scraped data
  python3 i18n.py export    # write translation jobs to translations/jobs_N.json
  python3 i18n.py import    # load translations/out_*.json into the i18n tables
  python3 i18n.py fixes     # apply translations/halal_text_fixes.json (pork/alcohol mentions)
  python3 i18n.py status    # coverage per language
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE / "davita_recipes.db"
TR = HERE / "translations"
LANGS = ("en", "es", "ar")
LIST_TABLES = ("ingredients", "steps", "hints")
MATCH_COLS = "calories, protein_g, carbohydrates_g, fat_g, sodium_mg, potassium_mg, phosphorus_mg"

SCHEMA = """
CREATE TABLE IF NOT EXISTS recipe_i18n (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id),
    lang TEXT NOT NULL,
    title TEXT, description TEXT, portions TEXT, serving_size TEXT,
    source TEXT NOT NULL,              -- davita | translated
    source_recipe_id INTEGER,          -- page the official text came from
    PRIMARY KEY (recipe_id, lang)
);
CREATE TABLE IF NOT EXISTS ingredients_i18n (recipe_id INTEGER, lang TEXT, position INTEGER, group_label TEXT, text TEXT, PRIMARY KEY (recipe_id, lang, position));
CREATE TABLE IF NOT EXISTS steps_i18n       (recipe_id INTEGER, lang TEXT, position INTEGER, group_label TEXT, text TEXT, PRIMARY KEY (recipe_id, lang, position));
CREATE TABLE IF NOT EXISTS hints_i18n       (recipe_id INTEGER, lang TEXT, position INTEGER, group_label TEXT, text TEXT, PRIMARY KEY (recipe_id, lang, position));
CREATE TABLE IF NOT EXISTS food_choices_i18n(recipe_id INTEGER, lang TEXT, position INTEGER, text TEXT, PRIMARY KEY (recipe_id, lang, position));
"""


def connect():
    db = sqlite3.connect(DB)
    cols = [r[1] for r in db.execute("PRAGMA table_info(recipes)")]
    if "canonical_id" not in cols:
        db.execute("ALTER TABLE recipes ADD COLUMN canonical_id INTEGER")
    db.executescript(SCHEMA)
    return db


def put(db, rid, lang, d, source, src_id=None):
    """Store one language version. d has title/description/portions/serving_size/ingredients/steps/hints/food_choices."""
    db.execute("INSERT OR REPLACE INTO recipe_i18n VALUES (?,?,?,?,?,?,?,?)",
               (rid, lang, d.get("title"), d.get("description"), d.get("portions"), d.get("serving_size"), source, src_id))
    for t in LIST_TABLES + ("food_choices",):
        db.execute(f"DELETE FROM {t}_i18n WHERE recipe_id=? AND lang=?", (rid, lang))
    for t in LIST_TABLES:
        db.executemany(f"INSERT INTO {t}_i18n VALUES (?,?,?,?,?)",
                       [(rid, lang, i, g, x) for i, (g, x) in enumerate(d.get(t) or [], 1)])
    db.executemany("INSERT INTO food_choices_i18n VALUES (?,?,?,?)",
                   [(rid, lang, i, x) for i, x in enumerate(d.get("food_choices") or [], 1)])


def source_text(db, rid):
    title, desc, por, srv = db.execute(
        "SELECT title, description, portions, serving_size FROM recipes WHERE id=?", (rid,)).fetchone()
    d = {"title": title, "description": desc, "portions": por, "serving_size": srv}
    for t in LIST_TABLES:
        d[t] = [[g, x] for g, x in db.execute(
            f"SELECT group_label, text FROM {t} WHERE recipe_id=? ORDER BY position", (rid,))]
    d["food_choices"] = [x for (x,) in db.execute(
        "SELECT text FROM food_choices WHERE recipe_id=? ORDER BY position", (rid,))]
    return d


def build():
    db = connect()
    # keep translations already imported; refresh the official (davita) text
    db.execute("DELETE FROM recipe_i18n WHERE source='davita'")
    en_by_nutrients = {}
    for row in db.execute(f"SELECT id, {MATCH_COLS} FROM recipes WHERE language='en'"):
        en_by_nutrients.setdefault(tuple(row[1:]), []).append(row[0])
    # external sources keep the canonical links set by import_sources.py
    db.execute("UPDATE recipes SET canonical_id = id WHERE site IN ('davita.com', 'espanol.davita.com')")
    for row in db.execute(f"SELECT id, {MATCH_COLS} FROM recipes WHERE language='es'").fetchall():
        match = en_by_nutrients.get(tuple(row[1:]), [])
        if len(match) == 1:
            db.execute("UPDATE recipes SET canonical_id=? WHERE id=?", (match[0], row[0]))
    for rid, lang, canon in db.execute("SELECT id, language, canonical_id FROM recipes").fetchall():
        put(db, canon, lang, source_text(db, rid), "davita", rid)
    db.commit()
    status(db)


def jobs(db):
    """Canonical recipes and the languages they still need."""
    out = []
    for (rid,) in db.execute("SELECT id FROM recipes WHERE canonical_id = id ORDER BY id"):
        have = {l: s for l, s in db.execute("SELECT lang, source FROM recipe_i18n WHERE recipe_id=?", (rid,))}
        need = [l for l in LANGS if l not in have]
        if need:
            src_lang = "en" if "en" in have else "es"
            d = {"title": None}
            row = db.execute("SELECT title, description, portions, serving_size FROM recipe_i18n WHERE recipe_id=? AND lang=?",
                             (rid, src_lang)).fetchone()
            d = dict(zip(("title", "description", "portions", "serving_size"), row))
            for t in LIST_TABLES:
                d[t] = [[g, x] for g, x in db.execute(
                    f"SELECT group_label, text FROM {t}_i18n WHERE recipe_id=? AND lang=? ORDER BY position", (rid, src_lang))]
            d["food_choices"] = [x for (x,) in db.execute(
                "SELECT text FROM food_choices_i18n WHERE recipe_id=? AND lang=? ORDER BY position", (rid, src_lang))]
            out.append({"id": rid, "source_lang": src_lang, "translate_to": need, **d})
    return out


def export(n_batches=None, prefix=None):
    """Write jobs_<prefix><i>.json for recipes still missing a language. A new prefix per run
    keeps earlier jobs/out files intact (import reads every out_*.json)."""
    db = connect()
    js = jobs(db)
    TR.mkdir(exist_ok=True)
    if prefix is None:
        used = {p.stem.split("_")[1].rstrip("0123456789") for p in TR.glob("jobs_*.json")}
        prefix = next(c for c in "abcdefghijklmnopqrstuvwxyz" if c not in used)
    n_batches = n_batches or max(1, -(-len(js) // 50))
    size = -(-len(js) // n_batches) if js else 0
    for i in range(n_batches):
        part = js[i * size:(i + 1) * size]
        if part:
            (TR / f"jobs_{prefix}{i}.json").write_text(json.dumps(part, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  translations/jobs_{prefix}{i}.json: {len(part)} recipes")
    print(f"{len(js)} recipes need translation, {sum(len(j['translate_to']) for j in js)} language versions")


def import_():
    db = connect()
    n = 0
    live = {r for (r,) in db.execute("SELECT id FROM recipes WHERE canonical_id = id")}
    for t in ("recipe_i18n",) + tuple(f"{x}_i18n" for x in LIST_TABLES + ("food_choices",)):
        db.execute(f"DELETE FROM {t} WHERE recipe_id NOT IN (SELECT id FROM recipes)")
    for f in sorted(TR.glob("out_*.json")):
        for rec in json.loads(f.read_text(encoding="utf-8")):
            if rec["id"] not in live:
                continue  # removed since translation (e.g. by the halal filter)
            for lang, d in rec["translations"].items():
                exists = db.execute("SELECT source FROM recipe_i18n WHERE recipe_id=? AND lang=?", (rec["id"], lang)).fetchone()
                if exists and exists[0] == "davita":
                    continue  # never overwrite official text
                put(db, rec["id"], lang, d, "translated")
                n += 1
    db.commit()
    print(f"imported {n} language versions")
    status(db)


def apply_fixes():
    """Apply translations/halal_text_fixes.json: rewrite or delete text that mentions pork or alcohol."""
    db = connect()
    path = TR / "halal_text_fixes.json"
    if not path.exists():
        print("no halal_text_fixes.json"); return
    # the review file holds the text each fix was written against; a fix only applies while the
    # stored text still equals it, so running this twice (or after renumbering) changes nothing
    originals = json.loads((TR / "halal_text_review.json").read_text(encoding="utf-8"))
    changed = deleted = 0
    for fx, orig in zip(json.loads(path.read_text(encoding="utf-8")), originals):
        rid, pos, field = fx["recipe_id"], fx["position"], fx["field"]
        assert (rid, pos, field) == (orig["recipe_id"], orig["position"], orig["field"]), "fixes/review files out of step"
        for lang, new in fx["text"].items():
            was = orig["text"].get(lang)
            if new == was:
                continue
            if field == "description":
                changed += db.execute("UPDATE recipe_i18n SET description=? WHERE recipe_id=? AND lang=? AND description=?",
                                      (new, rid, lang, was)).rowcount
                continue
            table = f"{field}_i18n"
            old = db.execute(f"SELECT text FROM {table} WHERE recipe_id=? AND lang=? AND position=?", (rid, lang, pos)).fetchone()
            if not old or old[0] != was:
                continue
            if new is None:
                db.execute(f"UPDATE {table} SET text=NULL WHERE recipe_id=? AND lang=? AND position=?", (rid, lang, pos))
                deleted += 1
            elif new != old[0]:
                db.execute(f"UPDATE {table} SET text=? WHERE recipe_id=? AND lang=? AND position=?", (new, rid, lang, pos))
                changed += 1
    # drop deleted items and close the gaps in numbering
    for table in ("steps_i18n", "hints_i18n"):
        gaps = db.execute(f"SELECT DISTINCT recipe_id, lang FROM {table} WHERE text IS NULL").fetchall()
        db.execute(f"DELETE FROM {table} WHERE text IS NULL")
        for rid, lang in gaps:
            rows = db.execute(f"SELECT position, group_label, text FROM {table} WHERE recipe_id=? AND lang=? ORDER BY position",
                              (rid, lang)).fetchall()
            db.execute(f"DELETE FROM {table} WHERE recipe_id=? AND lang=?", (rid, lang))
            db.executemany(f"INSERT INTO {table} VALUES (?,?,?,?,?)",
                           [(rid, lang, i, g, t) for i, (_, g, t) in enumerate(rows, 1)])
    db.commit()
    print(f"halal text fixes: {changed} rewritten, {deleted} removed")


def status(db=None):
    db = db or connect()
    total = db.execute("SELECT count(*) FROM recipes WHERE canonical_id = id").fetchone()[0]
    print(f"{total} recipes")
    for lang in LANGS:
        rows = dict(db.execute("SELECT source, count(*) FROM recipe_i18n WHERE lang=? GROUP BY source", (lang,)).fetchall())
        print(f"  {lang}: official {rows.get('davita', 0)}, translated {rows.get('translated', 0)}, "
              f"missing {total - sum(rows.values())}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"build": build, "export": export, "import": import_, "fixes": apply_fixes, "status": status}[cmd]()
