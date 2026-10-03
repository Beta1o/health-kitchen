#!/usr/bin/env python3
"""Build the recipe gallery from davita_recipes.db.

Outputs:
  gallery/index.html       the app, all recipe data inline (open it directly)
  gallery/thumbs/<id>.webp thumbnails used when the page is opened from disk
  gallery/photos/<id>.webp sharp 1280px photos for the recipe page
  gallery/img/chunk-N.json the same thumbnails packed as data URIs, used when the
                           page is served over http (e.g. the published artifact)
  gallery/artifact.html    the same app without the <html> wrapper, for publishing

Usage: python3 build_gallery.py
"""
import base64
import hashlib
import json
import os
import shutil
import re
import sqlite3
from pathlib import Path

from PIL import Image

from terms_i18n import ES_TO_EN, TERMS

HERE = Path(__file__).resolve().parent
DB = HERE / "davita_recipes.db"
OUT = HERE / "gallery"
THUMBS = OUT / "thumbs"
CHUNKS = OUT / "img"
TEMPLATE = HERE / "gallery_template.html"
THUMB_W = 520
PHOTO_W = 1280
PHOTOS = OUT / "photos"
CHUNK_SIZE = 90
LANGS = ("en", "es", "ar", "ur", "hi", "fr", "id", "bn", "tl")

NUTRIENTS = ["calories", "protein_g", "carbohydrates_g", "fat_g", "cholesterol_mg", "sodium_mg",
             "potassium_mg", "phosphorus_mg", "calcium_mg", "fiber_g", "added_sugar_g"]
TAX_KEYS = {"diet_type": "diet", "dish_type": "dish", "cuisine": "cuisine",
            "holiday": "holiday", "cooking_method": "method"}


def load_rgb(src: Path):
    """Open an image as RGB; cut-out photos with transparency get a soft light backdrop instead of black."""
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (243, 246, 242, 255))
        bg.alpha_composite(im)
        im = bg
    return im.convert("RGB")


def make_photo(src: Path, dst: Path):
    """Sharp copy for the recipe page (opened from disk or served next to the page)."""
    if not dst.exists():
        im = load_rgb(src)
        if im.width > PHOTO_W:
            im = im.resize((PHOTO_W, round(im.height * PHOTO_W / im.width)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=78, method=6)


def make_thumb(src: Path, dst: Path) -> bytes:
    if not dst.exists():
        im = load_rgb(src)
        if im.width > THUMB_W:
            im = im.resize((THUMB_W, round(im.height * THUMB_W / im.width)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=70, method=6)
    return dst.read_bytes()


def servings(portions):
    m = re.match(r"\s*(\d+)", portions or "")
    return int(m.group(1)) if m else None


def main():
    THUMBS.mkdir(parents=True, exist_ok=True)
    PHOTOS.mkdir(parents=True, exist_ok=True)
    CHUNKS.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row

    def text(rid, lang):
        row = db.execute("SELECT * FROM recipe_i18n WHERE recipe_id=? AND lang=?", (rid, lang)).fetchone()
        if not row:
            return None
        lists = {t: [[r["group_label"], r["text"]] for r in db.execute(
            f"SELECT group_label, text FROM {t}_i18n WHERE recipe_id=? AND lang=? ORDER BY position", (rid, lang))]
            for t in ("ingredients", "steps", "hints")}
        return {"title": row["title"], "desc": row["description"], "portions": row["portions"],
                "serving": row["serving_size"], "ing": lists["ingredients"], "steps": lists["steps"],
                "hints": lists["hints"],
                "choices": [r["text"] for r in db.execute(
                    "SELECT text FROM food_choices_i18n WHERE recipe_id=? AND lang=? ORDER BY position", (rid, lang))],
                "tr": 1 if row["source"] == "translated" else 0}

    def tags(page_ids):
        """Taxonomy values (English keys) across the English and Spanish pages of a recipe."""
        out = {v: set() for v in TAX_KEYS.values()}
        for pid in page_ids:
            for r in db.execute("SELECT rt.taxonomy, t.name FROM recipe_terms rt JOIN terms t ON t.id = rt.term_id "
                                "WHERE rt.recipe_id=?", (pid,)):
                if r["taxonomy"] not in TAX_KEYS:
                    continue
                name = ES_TO_EN.get(r["name"], r["name"]) if 1_000_000 <= pid < 2_000_000 else r["name"]
                key = TAX_KEYS[r["taxonomy"]]
                if name == "Budget":
                    key = "dish"
                out[key].add(name)
        return {k: sorted(v) for k, v in out.items()}

    recipes, chunk, chunk_no = [], {}, 0

    def flush():
        nonlocal chunk, chunk_no
        if chunk:
            # write next to the old file and swap, so a page loading during a rebuild never finds it missing
            tmp = CHUNKS / f".chunk-{chunk_no}.tmp"
            tmp.write_text(json.dumps(chunk))
            os.replace(tmp, CHUNKS / f"chunk-{chunk_no}.json")
            chunk, chunk_no = {}, chunk_no + 1

    rows = db.execute("SELECT * FROM recipes WHERE canonical_id = id ORDER BY title COLLATE NOCASE").fetchall()
    for r in rows:
        rid = r["id"]
        pages = {p["language"]: p for p in db.execute("SELECT * FROM recipes WHERE canonical_id=?", (rid,))}
        image_row = next((p for p in (r, *pages.values()) if p["image_path"]), None)
        img = None
        if image_row and (HERE / image_row["image_path"]).exists():
            data = make_thumb(HERE / image_row["image_path"], THUMBS / f"{rid}.webp")
            make_photo(HERE / image_row["image_path"], PHOTOS / f"{rid}.webp")
            img = 0   # has a photo: thumbs/<id>.webp and photos/<id>.webp
        t = {lang: text(rid, lang) for lang in LANGS}
        src = r["language"]
        cat = r["category_en"]
        tg = tags([p["id"] for p in pages.values()])
        tg.pop("holiday")  # occasions are not shown in the gallery
        recipes.append({
            "id": rid, "src": src, "url": r["url"],
            "urlEs": pages["es"]["url"] if "es" in pages and src == "en" else None,
            "cat": cat, "img": img, "by": r["submitted_by"], "sourceName": r["source_name"] or "DaVita",
            "carb": r["carbohydrate_choices"], "footnote": r["nutrition_footnote"],
            "n": [r[c] for c in NUTRIENTS],
            "video": r["video_url"] or next((p["video_url"] for p in pages.values() if p["video_url"]), None),
            "vtt": r["video_subtitles_url"],
            "serv": servings(r["portions"]),
            **tg,
            "modified": (r["date_modified"] or "")[:10],
            "t": {k: v for k, v in t.items() if v},
        })
    # thumbnails are served one file per recipe now; the old packed chunks are no longer used
    if CHUNKS.exists():
        shutil.rmtree(CHUNKS)

    # cuisines: one "American", "Latin American" for South America, and Middle Eastern split by country
    rename = {"Native American": "American", "Southern": "American", "South American": "Latin American", "Latin": "Latin American", "Venezuelan": "Latin American", "North Africa": "North African", "Jewish": "Eastern European"}
    by_dish = json.loads((HERE / "translations" / "cuisine_me.json").read_text(encoding="utf-8"))
    for rec in recipes:
        cu = {rename.get(c, c) for c in rec["cuisine"]}
        if "Middle Eastern" in cu:
            cu.discard("Middle Eastern")
            if str(rec["id"]) in by_dish:
                cu.add(by_dish[str(rec["id"])])
        rec["cuisine"] = sorted(cu)

    # reviewed categories for recipes from external sources (translations/catfix/out_*.json)
    catfix = {}
    for f in sorted((HERE / "translations" / "catfix").glob("out_*.json")):
        catfix.update(json.loads(f.read_text(encoding="utf-8")))
    for rec in recipes:
        if str(rec["id"]) in catfix:
            rec["cat"] = catfix[str(rec["id"])]

    # feminine Arabic steps/hints (translations/arf/out_*.json), shown when the reader picks "woman"
    arf = {}
    for f in sorted((HERE / "translations" / "arf").glob("out_*.json")):
        if "part" in f.stem:
            continue
        for o in json.loads(f.read_text(encoding="utf-8")):
            arf[o["id"]] = o
    for rec in recipes:
        o, ar = arf.get(rec["id"]), rec["t"].get("ar")
        if o and ar and len(o.get("steps") or []) == len(ar["steps"]) and len(o.get("hints") or []) == len(ar["hints"]):
            rec["t"]["arf"] = {**ar, "steps": o["steps"], "hints": o["hints"]}

    used = {v for rec in recipes for k in ("diet", "dish", "cuisine", "method") for v in rec[k]}
    used |= {rec["cat"] for rec in recipes}
    terms = {k: {"es": TERMS[k][0], "ar": TERMS[k][1]} for k in sorted(used) if k in TERMS}
    missing = sorted(used - set(TERMS))
    if missing:
        print("warning: no translation for", missing)

    # split text by language: core data keeps English (or the source text) and a list of available
    # languages; every other language goes to text/<lang>.js, loaded only when the reader picks it
    TEXT = OUT / "text"; TEXT.mkdir(exist_ok=True)
    per_lang = {}
    for rec in recipes:
        rec["L"] = sorted(k for k in rec["t"] if k != "arf")
        keep = "en" if "en" in rec["t"] else rec["src"]
        for k, v in list(rec["t"].items()):
            if k != keep:
                per_lang.setdefault(k, {})[rec["id"]] = v
        rec["t"] = {keep: rec["t"][keep]}
    vers = {}
    for k, m in per_lang.items():
        js = json.dumps(m, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        vers[k] = hashlib.md5(js.encode()).hexdigest()[:8]
        (TEXT / f"{k}.js").write_text(f"HK_TEXT({json.dumps(k)},{js});", encoding="utf-8")
    # interface strings for added languages (translations/ui/<lang>.js)
    UIDIR = OUT / "ui"; UIDIR.mkdir(exist_ok=True)
    for f in (HERE / "translations" / "ui").glob("*.js"):
        shutil.copy(f, UIDIR / f.name)
        vers["ui_" + f.stem] = hashlib.md5(f.read_bytes()).hexdigest()[:8]

    payload = {"recipes": recipes, "chunks": chunk_no, "terms": terms, "vers": vers,
               "excluded": db.execute("SELECT count(*) FROM excluded_recipes").fetchone()[0]}
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    # fonts (built by fonts/fetch_fonts.py) go in their own cached file instead of inside every page load
    fonts = (HERE / "fonts" / "fonts.css").read_text(encoding="utf-8")
    (OUT / "fonts.css").write_text(fonts, encoding="utf-8")
    fver = hashlib.md5(fonts.encode()).hexdigest()[:8]
    tpl = TEMPLATE.read_text(encoding="utf-8").replace("/*__FONTS__*/", "")
    (OUT / "data.js").write_text("window.HK_DATA=" + data + ";", encoding="utf-8")
    ver = hashlib.md5(data.encode()).hexdigest()[:8]
    # hosted accounts (Supabase): the project URL and the public anon key, from supabase.json (both are safe to publish)
    sbcfg = HERE / "supabase.json"
    sbjs = ""
    if sbcfg.exists():
        c = json.loads(sbcfg.read_text(encoding="utf-8"))
        if c.get("url") and c.get("anonKey"):
            sbjs = "<script>window.HK_SUPABASE=" + json.dumps({"url": c["url"], "anonKey": c["anonKey"]}) + ";</script>"
    # start downloading the reader's language files together with data.js (they are needed before the first paint)
    early = ("<script>(function(){try{var V=" + json.dumps({k: v for k, v in vers.items()}) + ",g=function(k){return JSON.parse(localStorage.getItem(k)||'null')},"
             "l=g('kk:lang')||((g('kk:cfgCache')||{}).defaults||{}).lang||(navigator.language||'en').slice(0,2);"
             "[['text/',l],['ui/','ui_'+l]].concat(l==='ar'?[['text/','arf']]:[]).forEach(function(p){var n=p[0]==='ui/'?l:p[1],v=V[p[1]];if(!v)return;var e=document.createElement('link');"
             "e.rel='preload';e.as='script';e.href=p[0]+n+'.js?v='+v;document.head.appendChild(e)})}catch(e){}})();</script>")
    body = tpl.replace("<!--__DATA_SCRIPT__-->", sbjs + early + f'<script src="data.js?v={ver}"></script>').replace("/*__DATA__*/null", "null")
    page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="description" content="Health Kitchen: thousands of recipes for kidney disease, diabetes, blood pressure and heart health, '
            'in 9 languages, with nutrition per serving, portions sized to your plan and meal plans.">\n'
            f'<link rel="preload" href="fonts.css?v={fver}" as="style">\n<link rel="stylesheet" href="fonts.css?v={fver}">\n'
            '</head>\n<body>\n' + body + '\n</body>\n</html>\n')
    (OUT / "index.html").write_text(page, encoding="utf-8")
    cover = {lang: sum(1 for x in recipes if lang in x["L"]) for lang in LANGS}
    print(f"{len(recipes)} recipes, {sum(1 for x in recipes if x['img'] is not None)} photos, {chunk_no} image chunks, "
          f"language coverage {cover}, index.html {(OUT / 'index.html').stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
