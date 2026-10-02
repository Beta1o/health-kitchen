#!/usr/bin/env python3
"""Download the gallery fonts once (latin, latin-ext, arabic subsets) and write fonts.css
with every face embedded as a base64 data URI, so the app never fetches fonts at runtime
and the page doesn't reflow when fonts arrive.

Usage: python3 fonts/fetch_fonts.py
"""
import base64
import re
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
CSS_URL = ("https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700"
           "&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=IBM+Plex+Mono:wght@500;600"
           "&family=IBM+Plex+Sans+Arabic:wght@400;700&family=Noto+Kufi+Arabic:wght@700;800&display=swap")
KEEP = {"latin", "latin-ext", "arabic"}


def main():
    css = requests.get(CSS_URL, headers={"User-Agent": UA}, timeout=30).text
    out, total = [], 0
    for subset, block in re.findall(r"/\* ([a-z-]+) \*/\s*(@font-face\s*{[^}]+})", css):
        if subset not in KEEP:
            continue
        url = re.search(r"url\((https://[^)]+)\)", block).group(1)
        name = HERE / ("cache_" + re.sub(r"[^a-zA-Z0-9]", "_", url.split("/s/")[-1]))
        if not name.exists():
            name.write_bytes(requests.get(url, headers={"User-Agent": UA}, timeout=60).content)
        data = name.read_bytes()
        total += len(data)
        block = block.replace(url, "data:font/woff2;base64," + base64.b64encode(data).decode())
        block = block.replace("font-display: swap", "font-display: block")
        out.append(f"/* {subset} */\n{block}")
    (HERE / "fonts.css").write_text("\n".join(out), encoding="utf-8")
    print(f"{len(out)} font faces, {total / 1024:.0f} KB of woff2 -> fonts.css")


if __name__ == "__main__":
    main()
