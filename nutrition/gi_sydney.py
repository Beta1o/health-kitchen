#!/usr/bin/env python3
"""Glycemic index data from the University of Sydney GI database (https://glycemicindex.com/gi-search/).

  python3 nutrition/gi_sydney.py          # download once -> nutrition/gi_sydney.json (prints a report)

The search page holds the whole database as one table, so this is a single page request (no query
strings: robots.txt disallows them). GI is measured against glucose = 100. Foods with pork, gelatin or
alcohol are left out, using the recipe ingredient policy (ingredient_filter.py) plus words that only
appear in food tables (jelly, gummies, cider, ...).

Values are kept as published. Copyright: © GI News, University of Sydney (https://glycemicindex.com,
https://ginews.blogspot.com). Free use with that notice and a link back; see
https://glycemicindex.com/copyright-and-permission/.
"""
import html
import json
import re
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ingredient_filter import check   # noqa: E402

URL = "https://glycemicindex.com/gi-search/"
OUT = HERE / "gi_sydney.json"
# food-table words the recipe policy does not cover: gelatin sweets and desserts, alcoholic drinks
EXTRA = re.compile(r"\bjelly crystals\b|^jelly\b|\bjelly beans?\b|\bgumm(y|ies)\b|\bjubes?\b|\bmarshmallow|\bgelatine?\b|"
                   r"\brum balls?\b|\bcider\b(?!\s*vinegar)|\bale\b|\bport wine|\bmead\b(?! johnson)|\bkirsch|\bliqueur|\bbeer\b(?<!ginger beer)|"
                   r"\bwine\b(?!\s*vinegar)|\bham\b|\bbacon\b|\bpork\b|\bsalami\b|\blard\b", re.I)
# names only (makers such as "Mead Johnson" are not foods); vanilla "bourbon", "champagne" rhubarb and plant
# starch jellies stay
SAFE = re.compile(r"bourbon vanilla|champagne rhubarb|starch jelly|herbal jelly|jelly consistency", re.I)
# "jelly" in UK/Australian names is the gelatin dessert; fruit spreads are named jam
COLS = ["name", "gi", "maker", "category", "country", "serving_g", "carbs_g", "gl", "ref", "subjects", "time", "n", "year"]


def num(v):
    try:
        return float(v.replace(",", "."))
    except ValueError:
        return None


def main():
    page = requests.get(URL, headers={"User-Agent": "HealthKitchen/1.0 (recipe app; GI data import)"}, timeout=120).text
    t = page[page.index('<table id="tablepress-1"'):]
    t = t[:t.index("</table>")]
    rows = []
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S)[1:]:
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)]
        if len(cells) == len(COLS):
            rows.append(dict(zip(COLS, cells)))
    kept, dropped, seen = [], [], set()
    for r in rows:
        if tuple(r.values()) in seen:   # some foods are listed twice
            continue
        seen.add(tuple(r.values()))
        name = r["name"]
        bad = not SAFE.search(name) and (check([name]) or EXTRA.search(name))
        if bad or num(r["gi"]) is None:
            dropped.append(r["name"])
            continue
        for k in ("gi", "serving_g", "carbs_g", "gl"):
            r[k] = num(r[k])
        kept.append(r)
    OUT.write_text(json.dumps({"source": URL, "copyright": "© GI News, University of Sydney", "foods": kept},
                              ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(rows)} foods, kept {len(kept)}, left out {len(dropped)} (pork, gelatin, alcohol or no GI)")
    for n in dropped[:40]:
        print("  -", n)


if __name__ == "__main__":
    main()
