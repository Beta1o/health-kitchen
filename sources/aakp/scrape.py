#!/usr/bin/env python3
"""Scraper for AAKP kidney-friendly recipes (AAKP Delicious! PDFs + HTML recipe posts).

Sources:
  * https://aakp.org/center-for-patient-research-and-education/kidney-friendly-recipes/
    -> links to 9 "AAKP Delicious!" edition pages, each listing recipe-card PDFs.
  * https://aakp.org/category/recipe/  (paginated WordPress category of HTML recipe posts)

The WP REST API (/wp-json/) sits behind a Cloudflare managed challenge, so it is not used.
Only requests + stdlib: PDFs are parsed with a small built-in PDF text extractor.

Re-runnable: raw pages/PDFs are cached under sources/aakp/cache/.
Usage: python3 scrape.py [--fetch-only]
"""
import difflib
import hashlib
import html as htmlmod
import json
import math
import os
import re
import struct
import sys
import time
import zlib
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, unquote

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
IMAGES = os.path.join(HERE, "images")
KEY = "aakp"
SOURCE_NAME = "AAKP"
BASE = "https://aakp.org"
LISTING = BASE + "/center-for-patient-research-and-education/kidney-friendly-recipes/"
CATEGORY = BASE + "/category/recipe/"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})


class Blocked(Exception):
    pass


def cache_path(url):
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", unquote(url.split("://", 1)[-1]))[-150:]
    h = hashlib.md5(url.encode()).hexdigest()[:8]
    return os.path.join(CACHE, h + "_" + name)


def fetch(url, binary=False, retries=6):
    """GET with cache; only cache good responses. Raises Blocked on challenge / persistent failure."""
    p = cache_path(url)
    if os.path.exists(p) and os.path.getsize(p) > 200:
        with open(p, "rb") as f:
            data = f.read()
        return data if binary else data.decode("utf-8", "replace")
    last = None
    for attempt in range(retries):
        try:
            r = SESSION.get(url, timeout=150)
        except requests.RequestException as e:
            last = str(e)
            time.sleep(5 * (attempt + 1))
            continue
        body = r.content
        if r.status_code == 200 and len(body) > 200:
            head = body[:3000]
            if b"<title>Just a moment...</title>" in head:
                raise Blocked("Cloudflare challenge")
            if binary and not body.startswith(b"%PDF") and b"<html" in head.lower():
                raise Blocked("non-PDF response")
            os.makedirs(CACHE, exist_ok=True)
            with open(p + ".tmp", "wb") as f:
                f.write(body)
            os.replace(p + ".tmp", p)
            return body if binary else body.decode("utf-8", "replace")
        if r.status_code == 404:
            raise Blocked("HTTP 404")
        if r.status_code == 403:
            raise Blocked("HTTP 403")
        last = "HTTP %s" % r.status_code
        time.sleep(min(60, 5 * 2 ** attempt))
    raise Blocked("failed after retries: %s" % last)


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------
def clean_text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s).replace("\xa0", " ").replace("​", "")
    return re.sub(r"\s+", " ", s).strip(" •\t\r\n")


def slugify(s):
    s = htmlmod.unescape(s).lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def content_block(page):
    i = page.find('class="entry-content')
    if i < 0:
        i = page.find("<main")
    seg = page[i:]
    for end in ('<footer class="entry-footer', "Categories</h2>", ">Categories<"):
        j = seg.find(end)
        if j > 0:
            seg = seg[:j]
            break
    return seg


def edition_number(url):
    m = re.search(r"(\d+)(?:st|nd|rd|th)-edition", url)
    return int(m.group(1))


def list_editions():
    page = fetch(LISTING)
    eds = sorted(set(re.findall(r'href="(https://aakp\.org/aakp-delicious-recipes-?\d+(?:st|nd|rd|th)-edition/)"', page)),
                 key=edition_number)
    others = []
    seg = content_block(page)
    for href, txt in re.findall(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', seg, re.S):
        others.append((urljoin(LISTING, htmlmod.unescape(href)), clean_text(txt)))
    return eds, others


def list_edition_pdfs(ed_url):
    """Return (claimed_count, [(pdf_url, title)]) with adjacent split links merged."""
    page = fetch(ed_url)
    seg = content_block(page)
    m = re.search(r"all (\d+) [Rr]ecipes", clean_text(seg))
    claimed = int(m.group(1)) if m else None
    out = []
    for href, txt in re.findall(r'<a [^>]*href="([^"]+\.pdf)"[^>]*>(.*?)</a>', seg, re.S):
        url = urljoin(ed_url, htmlmod.unescape(href).strip())
        t = clean_text(txt)
        if not t:
            continue
        if out and out[-1][0] == url and (t.startswith(out[-1][1]) or out[-1][1].startswith(t)):
            # one title split over two <a> tags pointing at the same file
            out[-1] = (url, max(t, out[-1][1], key=len))
            continue
        out.append((url, t))
    return claimed, out


def list_category_posts():
    posts, url, seen = [], CATEGORY, set()
    while url and url not in seen:
        seen.add(url)
        page = fetch(url)
        for href, title in re.findall(r'<h2 class="entry-title"><a href="([^"]+)" rel="bookmark">(.*?)</a>', page):
            posts.append((href, clean_text(title)))
        m = re.search(r'<a class="next page-numbers" href="([^"]+)"', page)
        url = htmlmod.unescape(m.group(1)) if m else None
    return posts


# ---------------------------------------------------------------------------
# Minimal PDF text extractor (stdlib only)
# ---------------------------------------------------------------------------
class Ref:
    __slots__ = ("num",)

    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return "R%d" % self.num


class Name(str):
    pass


class Op(str):
    pass


WS = b" \t\r\n\x00\x0c"
DELIM = b"()<>[]{}/%"


class Lexer:
    def __init__(self, data, pos=0):
        self.d = data
        self.i = pos
        self.n = len(data)

    def skip_ws(self):
        d, n = self.d, self.n
        while self.i < n:
            c = d[self.i]
            if c in WS:
                self.i += 1
            elif c == 0x25:  # %
                while self.i < n and d[self.i] not in b"\r\n":
                    self.i += 1
            else:
                break

    def token(self):
        """Return next token: numbers, Name, bytes (strings), Op, '[', ']', '<<', '>>', or None at EOF."""
        self.skip_ws()
        d, i = self.d, self.i
        if i >= self.n:
            return None
        c = d[i]
        if c == 0x2F:  # /
            j = i + 1
            while j < self.n and d[j] not in WS and d[j] not in DELIM:
                j += 1
            raw = d[i + 1:j]
            if b"#" in raw:
                raw = re.sub(rb"#([0-9A-Fa-f]{2})", lambda m: bytes([int(m.group(1), 16)]), raw)
            self.i = j
            return Name(raw.decode("latin-1"))
        if c == 0x28:  # (
            return self._literal()
        if c == 0x3C:  # <
            if i + 1 < self.n and d[i + 1] == 0x3C:
                self.i = i + 2
                return "<<"
            j = d.find(b">", i)
            hx = re.sub(rb"\s", b"", d[i + 1:j])
            if len(hx) % 2:
                hx += b"0"
            self.i = j + 1
            try:
                return bytes.fromhex(hx.decode("latin-1"))
            except ValueError:
                return b""
        if c == 0x3E:
            if i + 1 < self.n and d[i + 1] == 0x3E:
                self.i = i + 2
                return ">>"
            self.i = i + 1
            return Op(">")
        if c in b"[]{}":
            self.i = i + 1
            return chr(c)
        j = i
        while j < self.n and d[j] not in WS and d[j] not in DELIM:
            j += 1
        if j == i:
            j = i + 1
        w = d[i:j]
        self.i = j
        try:
            if b"." in w:
                return float(w)
            return int(w)
        except ValueError:
            return Op(w.decode("latin-1"))

    def _literal(self):
        d = self.d
        i = self.i + 1
        depth = 1
        out = bytearray()
        n = self.n
        while i < n:
            c = d[i]
            if c == 0x5C:  # backslash
                i += 1
                if i >= n:
                    break
                e = d[i]
                if e in b"01234567":
                    j = i
                    while j < i + 3 and j < n and d[j] in b"01234567":
                        j += 1
                    out.append(int(d[i:j], 8) & 0xFF)
                    i = j
                    continue
                m = {0x6E: 10, 0x72: 13, 0x74: 9, 0x62: 8, 0x66: 12}
                if e in m:
                    out.append(m[e])
                elif e == 0x0D:
                    if i + 1 < n and d[i + 1] == 0x0A:
                        i += 1
                elif e == 0x0A:
                    pass
                else:
                    out.append(e)
                i += 1
                continue
            if c == 0x28:
                depth += 1
            elif c == 0x29:
                depth -= 1
                if depth == 0:
                    i += 1
                    break
            out.append(c)
            i += 1
        self.i = i
        return bytes(out)


def parse_object(lex):
    """Parse one PDF object (handles refs 'n g R')."""
    t = lex.token()
    return _parse_from(lex, t)


def _parse_from(lex, t):
    if t == "<<":
        dct = {}
        while True:
            k = lex.token()
            if k == ">>" or k is None:
                return dct
            v = parse_object(lex)
            dct[str(k)] = v
    if t == "[":
        arr = []
        while True:
            save = lex.i
            k = lex.token()
            if k == "]" or k is None:
                return arr
            arr.append(_parse_from(lex, k))
    if isinstance(t, int):
        save = lex.i
        t2 = lex.token()
        if isinstance(t2, int):
            t3 = lex.token()
            if t3 == "R":
                return Ref(t)
        lex.i = save
        return t
    if isinstance(t, Op):
        if t == "true":
            return True
        if t == "false":
            return False
        if t == "null":
            return None
    return t


class PDF:
    def __init__(self, data):
        self.d = data
        self.objs = {}      # num -> (dict_or_value, stream_bytes_or_None)
        self._raw = {}
        self._scan()

    def _scan(self):
        d = self.d
        for m in re.finditer(rb"(?<![0-9])(\d+)\s+(\d+)\s+obj\b", d):
            self._raw[int(m.group(1))] = m.end()
        self.trailer_root = None
        for m in re.finditer(rb"/Root\s+(\d+)\s+\d+\s+R", d):
            self.trailer_root = int(m.group(1))
        # object streams
        for num, pos in list(self._raw.items()):
            head = d[pos:pos + 400]
            if b"/ObjStm" in head:
                try:
                    obj, stream = self.get(num, raw=True)
                except Exception:
                    continue
                if not isinstance(obj, dict) or obj.get("Type") != "ObjStm" or stream is None:
                    continue
                n = obj.get("N", 0)
                first = obj.get("First", 0)
                lex = Lexer(stream)
                pairs = []
                for _ in range(n):
                    a = lex.token()
                    b = lex.token()
                    pairs.append((a, b))
                for onum, off in pairs:
                    if onum in self._raw and not isinstance(self._raw[onum], tuple):
                        continue  # direct object wins
                    self._raw[onum] = ("objstm", stream, first + off)

    def get(self, num, raw=False):
        if num in self.objs:
            return self.objs[num]
        loc = self._raw.get(num)
        if loc is None:
            return (None, None)
        if isinstance(loc, tuple):
            lex = Lexer(loc[1], loc[2])
            val = parse_object(lex)
            res = (val, None)
            self.objs[num] = res
            return res
        lex = Lexer(self.d, loc)
        val = parse_object(lex)
        stream = None
        if isinstance(val, dict):
            lex.skip_ws()
            if self.d.startswith(b"stream", lex.i):
                s = lex.i + 6
                if self.d[s:s + 2] == b"\r\n":
                    s += 2
                elif self.d[s:s + 1] in (b"\n", b"\r"):
                    s += 1
                length = val.get("Length")
                if isinstance(length, Ref):
                    length = self.get(length.num)[0]
                e = None
                if isinstance(length, int) and self.d[s + length:s + length + 20].lstrip().startswith(b"endstream"):
                    e = s + length
                if e is None:
                    e = self.d.find(b"endstream", s)
                    while e > s and self.d[e - 1] in b"\r\n":
                        e -= 1
                rawbytes = self.d[s:e]
                stream = rawbytes if raw is None else self._decode(val, rawbytes)
                val["_raw_stream"] = rawbytes
        res = (val, stream)
        self.objs[num] = res
        return res

    def resolve(self, v):
        seen = 0
        while isinstance(v, Ref) and seen < 20:
            v = self.get(v.num)[0]
            seen += 1
        return v

    def stream_of(self, v):
        if isinstance(v, Ref):
            return self.get(v.num)
        return (v, None)

    def _decode(self, dct, data):
        filt = self.resolve(dct.get("Filter"))
        if filt is None:
            return data
        filts = filt if isinstance(filt, list) else [filt]
        parms = self.resolve(dct.get("DecodeParms"))
        for f in filts:
            f = self.resolve(f)
            if f in ("FlateDecode", "Fl"):
                try:
                    data = zlib.decompress(data)
                except zlib.error:
                    try:
                        data = zlib.decompressobj().decompress(data)
                    except zlib.error:
                        return b""
                if isinstance(parms, dict) and parms.get("Predictor", 1) >= 10:
                    data = _png_unpredict(data, parms.get("Columns", 1))
            elif f in ("DCTDecode", "DCT", "JPXDecode"):
                return data  # keep image bytes as-is
            elif f in ("ASCIIHexDecode", "AHx"):
                data = bytes.fromhex(re.sub(rb"[^0-9A-Fa-f]", b"", data.split(b">")[0]).decode())
            else:
                return b""
        return data

    # ---- page tree
    def pages(self):
        root = self.resolve(Ref(self.trailer_root)) if self.trailer_root else None
        out = []
        if isinstance(root, dict):
            self._walk(self.resolve(root.get("Pages")), {}, out, 0)
        if not out:  # fallback: any /Type /Page objects in number order
            for num in sorted(self._raw):
                o = self.get(num)[0]
                if isinstance(o, dict) and o.get("Type") == "Page":
                    out.append((o, self.resolve(o.get("Resources")) or {}))
        return out

    def _walk(self, node, inherited, out, depth):
        if not isinstance(node, dict) or depth > 30:
            return
        inh = dict(inherited)
        if "Resources" in node:
            inh["Resources"] = node["Resources"]
        if node.get("Type") == "Pages" or "Kids" in node:
            for k in self.resolve(node.get("Kids")) or []:
                self._walk(self.resolve(k), inh, out, depth + 1)
        else:
            out.append((node, self.resolve(inh.get("Resources")) or {}))


def _png_unpredict(data, columns):
    out = bytearray()
    row = columns + 1
    prev = bytearray(columns)
    for i in range(0, len(data), row):
        ft = data[i]
        cur = bytearray(data[i + 1:i + row])
        for j in range(len(cur)):
            a = cur[j - 1] if j else 0
            b = prev[j] if j < len(prev) else 0
            c = prev[j - 1] if j and j - 1 < len(prev) else 0
            if ft == 1:
                cur[j] = (cur[j] + a) & 255
            elif ft == 2:
                cur[j] = (cur[j] + b) & 255
            elif ft == 3:
                cur[j] = (cur[j] + (a + b) // 2) & 255
            elif ft == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                cur[j] = (cur[j] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        out += cur
        prev = cur
    return bytes(out)


# Glyph names -> unicode for simple fonts without ToUnicode
GLYPHS = {
    "space": " ", "exclam": "!", "quotedbl": '"', "numbersign": "#", "dollar": "$", "percent": "%",
    "ampersand": "&", "quotesingle": "'", "quoteright": "’", "quoteleft": "‘", "parenleft": "(",
    "parenright": ")", "asterisk": "*", "plus": "+", "comma": ",", "hyphen": "-", "period": ".",
    "slash": "/", "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "colon": ":", "semicolon": ";", "less": "<",
    "equal": "=", "greater": ">", "question": "?", "at": "@", "bracketleft": "[", "backslash": "\\",
    "bracketright": "]", "asciicircum": "^", "underscore": "_", "grave": "`", "braceleft": "{",
    "bar": "|", "braceright": "}", "asciitilde": "~", "bullet": "•", "endash": "–",
    "emdash": "—", "quotedblleft": "“", "quotedblright": "”", "ellipsis": "…",
    "degree": "°", "onehalf": "½", "onequarter": "¼", "threequarters": "¾",
    "onethird": "⅓", "twothirds": "⅔", "oneeighth": "⅛", "fraction": "⁄",
    "fi": "fi", "fl": "fl", "ff": "ff", "ffi": "ffi", "ffl": "ffl", "eacute": "é", "egrave": "è",
    "agrave": "à", "ccedilla": "ç", "ntilde": "ñ", "registered": "®",
    "trademark": "™", "copyright": "©", "minus": "-", "multiply": "×", "periodcentered": "·",
    "nbspace": " ", "uni00A0": " ", "Eacute": "É", "acircumflex": "â", "ecircumflex": "ê",
    "odieresis": "ö", "udieresis": "ü", "adieresis": "ä", "iacute": "í", "oacute": "ó",
    "aacute": "á", "uacute": "ú", "dagger": "†", "section": "§", "cent": "¢",
    "quotesinglbase": "‚", "quotedblbase": "„", "guillemotleft": "«", "guillemotright": "»",
    "plusminus": "±", "mu": "µ", "germandbls": "ß", "idieresis": "ï", "edieresis": "ë",
}


def glyph_to_uni(name):
    if name in GLYPHS:
        return GLYPHS[name]
    if len(name) == 1:
        return name
    m = re.match(r"^uni([0-9A-Fa-f]{4})", name)
    if m:
        return chr(int(m.group(1), 16))
    m = re.match(r"^u([0-9A-Fa-f]{4,6})$", name)
    if m:
        return chr(int(m.group(1), 16))
    base = name.split(".")[0].split("_")[0]
    if base != name:
        return glyph_to_uni(base)
    return ""


def _std_encoding(name):
    if name == "MacRomanEncoding":
        enc = {i: bytes([i]).decode("mac_roman") for i in range(32, 256)}
    else:  # WinAnsi / Standard (close enough for text)
        enc = {}
        for i in range(32, 256):
            try:
                enc[i] = bytes([i]).decode("cp1252")
            except UnicodeDecodeError:
                enc[i] = ""
        if name == "StandardEncoding":
            enc[0x27] = "’"
            enc[0x60] = "‘"
    return enc


def parse_cmap(data):
    """ToUnicode CMap -> (dict code_bytes_int->str, code_len)."""
    m = {}
    code_len = 1
    txt = data.decode("latin-1")
    cs = re.search(r"begincodespacerange\s*<([0-9A-Fa-f]+)>", txt)
    if cs:
        code_len = len(cs.group(1)) // 2

    def hexstr(h):
        b = bytes.fromhex(h)
        try:
            return b.decode("utf-16-be")
        except UnicodeDecodeError:
            return ""
    for block in re.findall(r"beginbfchar(.*?)endbfchar", txt, re.S):
        for a, b in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]*)>", block):
            m[int(a, 16)] = hexstr(b)
            code_len = max(code_len, len(a) // 2) if not cs else code_len
    for block in re.findall(r"beginbfrange(.*?)endbfrange", txt, re.S):
        for a, b, rest in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(\[[^\]]*\]|<[0-9A-Fa-f]*>)", block):
            lo, hi = int(a, 16), int(b, 16)
            if rest.startswith("["):
                items = re.findall(r"<([0-9A-Fa-f]*)>", rest)
                for k, h in enumerate(items):
                    m[lo + k] = hexstr(h)
            else:
                h = rest[1:-1]
                if not h:
                    continue
                base = int(h, 16)
                nb = len(h) // 2
                for k in range(0, min(hi - lo, 65535) + 1):
                    v = (base + k).to_bytes(nb, "big")
                    try:
                        m[lo + k] = v.decode("utf-16-be")
                    except UnicodeDecodeError:
                        m[lo + k] = ""
    return m, code_len


class Font:
    def __init__(self, pdf, fd):
        self.pdf = pdf
        fd = pdf.resolve(fd) or {}
        self.subtype = fd.get("Subtype")
        self.basefont = str(fd.get("BaseFont") or "")
        self.composite = self.subtype == "Type0"
        self.code_len = 2 if self.composite else 1
        self.tounicode = None
        tu = fd.get("ToUnicode")
        if isinstance(tu, Ref):
            _, data = pdf.get(tu.num)
            if data:
                self.tounicode, cl = parse_cmap(data)
                if self.composite:
                    self.code_len = cl or 2
        self.widths = {}
        self.dw = 1000 if self.composite else 500
        if self.composite:
            desc = pdf.resolve((pdf.resolve(fd.get("DescendantFonts")) or [None])[0]) or {}
            self.dw = pdf.resolve(desc.get("DW")) or 1000
            w = pdf.resolve(desc.get("W")) or []
            i = 0
            while i < len(w):
                a = pdf.resolve(w[i])
                b = pdf.resolve(w[i + 1]) if i + 1 < len(w) else None
                if isinstance(b, list):
                    for k, x in enumerate(b):
                        self.widths[a + k] = pdf.resolve(x)
                    i += 2
                else:
                    c = pdf.resolve(w[i + 2]) if i + 2 < len(w) else 0
                    for k in range(a, (b or a) + 1):
                        self.widths[k] = c
                    i += 3
        else:
            fc = pdf.resolve(fd.get("FirstChar")) or 0
            for k, x in enumerate(pdf.resolve(fd.get("Widths")) or []):
                self.widths[fc + k] = pdf.resolve(x)
            desc = pdf.resolve(fd.get("FontDescriptor")) or {}
            mw = pdf.resolve(desc.get("MissingWidth"))
            if mw:
                self.dw = mw
        self.enc = None
        if not self.composite:
            enc = pdf.resolve(fd.get("Encoding"))
            base = "StandardEncoding"
            diffs = []
            if isinstance(enc, str):
                base = enc
            elif isinstance(enc, dict):
                base = enc.get("BaseEncoding") or "StandardEncoding"
                diffs = pdf.resolve(enc.get("Differences")) or []
            self.enc = _std_encoding(base)
            code = 0
            for x in diffs:
                x = pdf.resolve(x)
                if isinstance(x, int):
                    code = x
                else:
                    self.enc[code] = glyph_to_uni(str(x))
                    code += 1

    def decode(self, b):
        """Yield (code, unicode_text, width_units)."""
        cl = self.code_len
        out = []
        for i in range(0, len(b) - cl + 1, cl):
            code = int.from_bytes(b[i:i + cl], "big")
            if self.tounicode is not None and code in self.tounicode:
                u = self.tounicode[code]
            elif self.enc is not None:
                u = self.enc.get(code, "")
            else:
                u = ""
            out.append((code, u, self.widths.get(code, self.dw)))
        return out


def _mul(a, b):
    return [a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5]]


def pdf_extract(data):
    """Return (spans, images). spans: dicts page,x,y,x2,size,text. images: (w,h,colorspace,bytes)."""
    pdf = PDF(data)
    spans, images = [], []
    font_cache = {}
    for pno, (page, res) in enumerate(pdf.pages()):
        streams = []
        c = page.get("Contents")
        if isinstance(c, Ref):
            obj, st = pdf.get(c.num)
            if st is not None:
                streams.append(st)
            elif isinstance(obj, list):
                c = obj
        if isinstance(c, list):
            for x in c:
                if isinstance(x, Ref):
                    streams.append(pdf.get(x.num)[1] or b"")
        _run_content(pdf, b"\n".join(streams), res, [1, 0, 0, 1, 0, 0], pno, spans, images, font_cache, 0)
    return spans, images


def _run_content(pdf, data, res, ctm, pno, spans, images, font_cache, depth):
    if depth > 8:
        return
    res = pdf.resolve(res) or {}
    fonts = pdf.resolve(res.get("Font")) or {}
    xobjs = pdf.resolve(res.get("XObject")) or {}
    lex = Lexer(data)
    stack = []
    gstack = []
    tm = [1, 0, 0, 1, 0, 0]
    tlm = [1, 0, 0, 1, 0, 0]
    font = None
    fs = 1.0
    tc = tw = 0.0
    th = 1.0
    tl = 0.0
    trise = 0.0
    fill = None

    def get_font(nm):
        ref = fonts.get(nm)
        key = ref.num if isinstance(ref, Ref) else id(ref)
        if key not in font_cache:
            font_cache[key] = Font(pdf, ref)
        return font_cache[key]

    def show(s):
        nonlocal tm
        if font is None:
            return
        trm0 = _mul([fs * th, 0, 0, fs, 0, trise], _mul(tm, ctm))
        x0, y0 = trm0[4], trm0[5]
        # text direction (0/90/180/270 deg); coordinates are rotated so that lines run left-to-right
        rot = int(round(math.degrees(math.atan2(trm0[1], trm0[0])) / 90.0)) % 4 * 90
        size = math.hypot(trm0[2], trm0[3])
        text = []
        for code, u, w in font.decode(s):
            adv = (w / 1000.0 * fs + tc + (tw if (font.code_len == 1 and code == 32) else 0)) * th
            text.append(u)
            tm = _mul([1, 0, 0, 1, adv, 0], tm)
        trm1 = _mul([fs * th, 0, 0, fs, 0, trise], _mul(tm, ctm))
        t = "".join(text)
        if "Wingdings" in font.basefont:   # dingbat glyphs used as check marks / bullets
            t = "".join("\uf0fc" if c == 0x39 else "\u2022" for c, _, _ in font.decode(s))
        x1 = trm1[4]
        if rot == 90:
            x0, y0, x1 = y0, -x0, trm1[5]
        elif rot == 180:
            x0, y0, x1 = -x0, -y0, -trm1[4]
        elif rot == 270:
            x0, y0, x1 = -y0, x0, -trm1[5]
        if t or s:
            spans.append({"page": pno, "x": round(x0, 2), "y": round(y0, 2), "x2": round(x1, 2), "rot": rot,
                          "size": round(size, 2), "text": t, "font": font.basefont,
                          "codes": s.hex(), "fill": fill})

    while True:
        t = lex.token()
        if t is None:
            break
        if not isinstance(t, Op):
            if t == "[":
                stack.append(_parse_from(lex, t))
            elif t == "<<":
                stack.append(_parse_from(lex, t))
            else:
                stack.append(t)
            continue
        op = str(t)
        try:
            if op == "BT":
                tm = [1, 0, 0, 1, 0, 0]
                tlm = [1, 0, 0, 1, 0, 0]
            elif op == "Tf":
                font = get_font(str(stack[-2]))
                fs = float(stack[-1])
            elif op == "Tm":
                tm = [float(x) for x in stack[-6:]]
                tlm = list(tm)
            elif op in ("Td", "TD"):
                tx, ty = float(stack[-2]), float(stack[-1])
                if op == "TD":
                    tl = -ty
                tlm = _mul([1, 0, 0, 1, tx, ty], tlm)
                tm = list(tlm)
            elif op == "T*":
                tlm = _mul([1, 0, 0, 1, 0, -tl], tlm)
                tm = list(tlm)
            elif op == "TL":
                tl = float(stack[-1])
            elif op == "Tc":
                tc = float(stack[-1])
            elif op == "Tw":
                tw = float(stack[-1])
            elif op == "Tz":
                th = float(stack[-1]) / 100.0
            elif op == "Ts":
                trise = float(stack[-1])
            elif op == "Tj":
                show(stack[-1])
            elif op == "'":
                tlm = _mul([1, 0, 0, 1, 0, -tl], tlm)
                tm = list(tlm)
                show(stack[-1])
            elif op == '"':
                tw, tc = float(stack[-3]), float(stack[-2])
                tlm = _mul([1, 0, 0, 1, 0, -tl], tlm)
                tm = list(tlm)
                show(stack[-1])
            elif op == "TJ":
                for item in stack[-1]:
                    if isinstance(item, bytes):
                        show(item)
                    elif isinstance(item, (int, float)):
                        adv = -item / 1000.0 * fs * th
                        tm = _mul([1, 0, 0, 1, adv, 0], tm)
            elif op in ("rg", "k", "g", "sc", "scn"):
                fill = tuple(round(float(v), 3) for v in stack if isinstance(v, (int, float)))
            elif op == "q":
                gstack.append((list(ctm), fill))
            elif op == "Q":
                if gstack:
                    ctm, fill = gstack.pop()
            elif op == "cm":
                ctm = _mul([float(x) for x in stack[-6:]], ctm)
            elif op == "Do":
                ref = xobjs.get(str(stack[-1]))
                if isinstance(ref, Ref):
                    xd, xs = pdf.get(ref.num)
                    if isinstance(xd, dict):
                        st = xd.get("Subtype")
                        if st == "Form":
                            m = pdf.resolve(xd.get("Matrix")) or [1, 0, 0, 1, 0, 0]
                            _run_content(pdf, xs or b"", xd.get("Resources") or res,
                                         _mul([float(v) for v in m], ctm), pno, spans, images, font_cache, depth + 1)
                        elif st == "Image":
                            filt = pdf.resolve(xd.get("Filter"))
                            filt = filt[-1] if isinstance(filt, list) and filt else filt
                            cs = pdf.resolve(xd.get("ColorSpace"))
                            if isinstance(cs, list):
                                cs = cs[0]
                            images.append({"page": pno, "w": xd.get("Width"), "h": xd.get("Height"),
                                           "filter": filt, "cs": str(cs), "ref": ref.num,
                                           "disp_w": abs(ctm[0]), "disp_h": abs(ctm[3]),
                                           "decode": pdf.resolve(xd.get("Decode")),
                                           "raw": xd.get("_raw_stream") if filt in ("DCTDecode", "DCT") else None})
            elif op == "BI":
                # inline image: skip to EI
                j = data.find(b"EI", lex.i)
                while j >= 0 and not (data[j - 1:j] in (b" ", b"\n", b"\r") and data[j + 2:j + 3] in (b" ", b"\n", b"\r", b"")):
                    j = data.find(b"EI", j + 2)
                lex.i = j + 2 if j >= 0 else len(data)
        except (IndexError, ValueError, TypeError, KeyError, AttributeError):
            pass
        stack = []


def spans_to_lines(spans, ytol=None):
    """Group spans into lines per page: list of dicts with page,y,x,size,text,spans."""
    lines = []
    for pno in sorted(set(s["page"] for s in spans)):
        ps = [s for s in spans if s["page"] == pno and s["text"].strip() != "" or (s["page"] == pno and s["text"] == " ")]
        ps.sort(key=lambda s: (-s["y"], s["x"]))
        cur = []
        for s in ps:
            if cur and abs(cur[0]["y"] - s["y"]) <= max(1.5, 0.3 * min(cur[0]["size"], s["size"])):
                cur.append(s)
            else:
                if cur:
                    lines.append(cur)
                cur = [s]
        if cur:
            lines.append(cur)
    return lines


def line_segments(line, colgap=1.6):
    """Join spans of one line into text segments; a big horizontal gap starts a new segment.
    Returns list of (x, x2, size, text)."""
    segs = []
    for s in sorted(line, key=lambda s: s["x"]):
        if s["size"] < 1:
            continue
        if segs and not s["text"].strip() and s["x"] < segs[-1][1] - 0.3:
            continue  # whitespace glyph drawn over the previous text (broken ligature)
        if segs:
            x, x2, size, txt = segs[-1]
            gap = s["x"] - x2
            ref = max(size, s["size"])
            if gap < colgap * ref and gap > -2 * ref:
                sep = ""
                if gap > 0.18 * ref and not txt.endswith(" ") and not s["text"].startswith(" "):
                    sep = " "
                segs[-1] = (x, max(x2, s["x2"]), max(size, s["size"]), txt + sep + s["text"])
                continue
        segs.append((s["x"], s["x2"], s["size"], s["text"]))
    return [(a, b, c, re.sub(r"\s+", " ", d).strip()) for a, b, c, d in segs if d.strip()]


# ---------------------------------------------------------------------------
# Recipe-card PDF parsing (layout based)
# ---------------------------------------------------------------------------
FOOTER_RE = re.compile(r"presented by|favorably reviewed|supported by|educational donation|\.indd|"
                       r"american association of kidney patients|^aakp\.org$|copyright|ebmed inc", re.I)
TEXT_FIXES = [
    (re.compile(r"\b([Mm])ufn"), r"\1uffin"),
    (re.compile(r"\bcofee\b"), "coffee"),
    (re.compile(r"\s+([,.;:)])"), r"\1"),
    (re.compile(r"\(\s+"), "("),
    (re.compile(r"\s{2,}"), " "),
]


def fix_text(t):
    t = t.replace(" ", " ").replace(" ", " ").replace(" ", " ").replace(" ", " ")
    t = t.replace("‑", "-").replace("­", "").replace("", "").replace("⁄", "/")
    for rx, rep in TEXT_FIXES:
        t = rx.sub(rep, t)
    return t.strip()


def _is_check(s):
    return s["text"] == "" or ("Wingdings" in s.get("font", "") and s.get("codes", "").endswith("39"))


def _is_white(fill):
    if not fill:
        return False
    if len(fill) == 4:
        return all(v <= 0.01 for v in fill)
    return all(v >= 0.99 for v in fill)


def _is_black(fill):
    if not fill:
        return True
    if len(fill) == 4:
        return fill[3] >= 0.9 and max(fill[:3]) <= 0.1
    if len(fill) == 1:
        return fill[0] <= 0.1
    return max(fill) <= 0.1


SUFFIXES = ("ents", "ent", "ment", "ments", "tion", "tions", "sion", "ing", "ings", "ed", "ly", "ness", "ble",
            "ture", "ous", "ic", "al", "er", "ers", "ate", "ated", "ize", "ized", "ity", "ies", "es", "able",
            "ible", "ance", "ence", "ant", "ive", "ful", "less", "ness", "ary", "ory", "um", "ue", "ry", "nal")


def join_wrapped(prev, nxt):
    """Join a wrapped line to the previous text, removing soft hyphenation."""
    m = re.search(r"([A-Za-z]{2,})-$", prev)
    if m and re.match(r"^[a-z]", nxt):
        right = re.match(r"^[a-z]+", nxt).group(0)
        if right in SUFFIXES:
            return prev[:-1] + nxt
        return prev + nxt
    return prev + " " + nxt


class Line:
    """One visual line inside a region: spans sorted by x."""

    def __init__(self, spans):
        self.spans = sorted(spans, key=lambda s: s["x"])
        self.page = spans[0]["page"]
        self.y = max(s["y"] for s in spans)
        self.x = self.spans[0]["x"]
        self.size = max(s["size"] for s in spans)
        segs = line_segments(self.spans, colgap=50)
        self.text = fix_text(" ".join(t for _, _, _, t in segs))
        first = next((s for s in self.spans if s["text"].strip()), self.spans[0])
        self.x = first["x"]
        self.first_font = first.get("font", "")
        self.first_fill = first.get("fill")

    @property
    def is_label(self):
        t = self.text
        return ("Bold" in self.first_font and not _is_black(self.first_fill) and not re.match(r"^[a-z]", t)
                and not t.endswith((".", ",")) and len(t.split()) <= 6
                and not re.match(r"^(note|notes|tips?|suggestions?|please note)\b", t, re.I))


def group_lines(spans):
    """spans (same page) -> list of Line, top to bottom."""
    spans = sorted([s for s in spans if s["text"].strip() or True], key=lambda s: (-s["y"], s["x"]))
    lines, cur = [], []
    for s in spans:
        if cur and abs(cur[0]["y"] - s["y"]) <= max(1.5, 0.3 * min(cur[0]["size"], s["size"])):
            cur.append(s)
        else:
            if cur:
                lines.append(cur)
            cur = [s]
    if cur:
        lines.append(cur)
    out = []
    for l in lines:
        if any(s["text"].strip() for s in l):
            L = Line(l)
            if L.text:
                out.append(L)
    return out


def _find_word_x(line_spans, word):
    """x of the span where `word` (lowercase, no spaces) starts in the joined line text."""
    acc, idx = "", []
    for s in sorted(line_spans, key=lambda s: s["x"]):
        for ch in s["text"]:
            if not ch.isspace():
                acc += ch.lower()
                idx.append(s)
    k = acc.find(word)
    if k < 0:
        return None
    return idx[k]["x"]


def _heading(spans_by_page, word):
    """Find a section heading (e.g. INGREDIENTS) as its own text segment: (page, x, y, size)."""
    others = ("ingredients", "preparation", "directions", "instructions", "method")
    for pno, spans in spans_by_page.items():
        for line in _raw_lines(spans):
            for g in segment_groups(line):
                t = re.sub(r"\s+", "", "".join(x["text"] for x in g).lower())
                if not t.startswith(word) and not any(t.startswith(o) and t[len(o):].startswith(word) for o in others):
                    continue
                rest = t.replace(word, "", 1)
                for o in others:
                    rest = rest.replace(o, "", 1)
                if rest.strip(":*") or ":" in t:
                    continue
                return (pno, _find_word_x(g, word), max(x["y"] for x in g), max(x["size"] for x in g))
    return None


def _raw_lines(spans):
    spans = sorted(spans, key=lambda s: (-s["y"], s["x"]))
    lines, cur = [], []
    for s in spans:
        if cur and abs(cur[0]["y"] - s["y"]) <= max(1.5, 0.3 * min(cur[0]["size"], s["size"])):
            cur.append(s)
        else:
            if cur:
                lines.append(cur)
            cur = [s]
    if cur:
        lines.append(cur)
    return lines


def segment_groups(line, colgap=1.6):
    """Like line_segments but returns the member spans of each segment."""
    groups = []
    for s in sorted(line, key=lambda s: s["x"]):
        if groups:
            g = groups[-1]
            x2 = max(t["x2"] for t in g)
            ref = max(max(t["size"] for t in g), s["size"])
            gap = s["x"] - x2
            if -2 * ref < gap < colgap * ref:
                g.append(s)
                continue
        groups.append([s])
    return groups


def strip_footer(spans):
    out = []
    for line in _raw_lines(spans):
        for g in segment_groups(line):
            txt = re.sub(r"\s+", " ", "".join(t["text"] for t in g))
            txt2 = " ".join(t for _, _, _, t in line_segments(g))
            if FOOTER_RE.search(txt) or FOOTER_RE.search(txt2):
                continue
            out.extend(g)
    return out


def _columns(spans, gap=25):
    """Column start x's from the starts of text segments (clusters with a 'real' line start)."""
    xs = []
    for line in _raw_lines(spans):
        for g in segment_groups(line):
            g2 = [t for t in g if t["text"].strip()]
            if g2:
                xs.append((min(t["x"] for t in g2), "".join(t["text"] for t in sorted(g2, key=lambda t: t["x"])).strip()))
    xs.sort()
    cols = []
    for x, t in xs:
        if not cols or x - cols[-1][-1][0] > gap:
            cols.append([(x, t)])
        else:
            cols[-1].append((x, t))
    good = [c[0][0] for c in cols if len(c) >= 2 and any(re.match(r"^[\d¼½¾⅓⅔⅛A-Z(•*\uf0fc]", t) for _, t in c)]
    return good or ([xs[0][0]] if xs else [])


def _split_by_columns(spans, starts):
    """Assign each span to the column with greatest start <= x+2."""
    buckets = {s: [] for s in starts}
    for sp in spans:
        c = None
        for st in starts:
            if sp["x"] + 2 >= st:
                c = st
        if c is None:
            c = starts[0]
        buckets[c].append(sp)
    return [buckets[s] for s in starts]


HEADING_WORDS = {"ingredients", "preparation", "directions", "instructions", "ingredientspreparation"}


def _is_heading_line(L):
    return re.sub(r"[\s:]+", "", L.text.lower()) in HEADING_WORDS


def parse_ingredient_region(spans):
    ingredients, hints = [], []
    if not spans:
        return ingredients, hints
    # footnotes ("* ...", small print) may run across sub-columns: take them out first
    foot, in_foot = [], False
    for L in group_lines(spans):
        small = all(x["size"] < 7.6 for x in L.spans if x["text"].strip())
        if (L.text.startswith("*") and not L.is_label) or (in_foot and small):
            foot.append(L)
            in_foot = True
        else:
            in_foot = False
    if foot:
        ids = set(id(x) for L in foot for x in L.spans)
        spans = [x for x in spans if id(x) not in ids]
        for L in foot:
            if L.text.startswith("*") or not hints:
                hints.append([None, L.text])
            else:
                hints[-1][1] = join_wrapped(hints[-1][1], L.text)
    if not spans:
        return ingredients, hints
    starts = _columns(spans)
    group = None
    for colspans in _split_by_columns(spans, starts):
        lines = group_lines(colspans)
        if not lines:
            continue
        base = min(L.x for L in lines)
        cur = None   # ('ing'|'hint', index)
        for L in lines:
            t = L.text
            if not t or _is_heading_line(L):
                continue
            if L.is_label and not re.match(r"^\d", t):
                group = t.strip("*: ")
                cur = None
                continue
            if t.startswith("*") or re.match(r"^(note|tips?)\b", t, re.I) or (L.size < 7.6 and cur and cur[0] != "hint"):
                hints.append([None, t])
                cur = ("hint", len(hints) - 1)
                continue
            if cur and cur[0] == "ing" and re.match(r"^[a-z]", t):
                prev = ingredients[cur[1]][1]
                if prev.count("(") > prev.count(")") or re.search(r"(,|\(|\b(and|or|such|of|with|to))$", prev):
                    ingredients[cur[1]] = [ingredients[cur[1]][0], join_wrapped(prev, t)]
                    continue
            if cur and L.x > base + 4.5:
                if cur[0] == "ing":
                    g, prev = ingredients[cur[1]]
                    ingredients[cur[1]] = [g, join_wrapped(prev, t)]
                else:
                    hints[cur[1]][1] += " " + t
                continue
            if cur and cur[0] == "hint" and L.size < 7.6:
                hints[cur[1]][1] += " " + t
                continue
            ingredients.append([group, t])
            cur = ("ing", len(ingredients) - 1)
    return ingredients, hints


HINT_HEAD_RE = re.compile(r"^(suggestions?|tips?|notes?|serving suggestions?|variations?)\s*:?\s*$", re.I)
HINT_START_RE = re.compile(r"^(\*|note\b|notes\b|tips?\b|suggestions?\b|please note|variation)", re.I)


def parse_prep_region(spans):
    steps, hints = [], []
    if not spans:
        return steps, hints
    # a SUGGESTIONS / TIPS block at the bottom runs across sub-columns: split it off first
    tail = []
    for L in group_lines(spans):
        if re.sub(r"[\s:]+", "", L.text.lower()) in ("suggestion", "suggestions", "tips", "tip", "notes",
                                                       "servingsuggestion", "servingsuggestions"):
            ycut = L.y + 1
            tail = [x for x in spans if x["y"] <= ycut]
            ids = set(id(x) for x in tail)
            spans = [x for x in spans if id(x) not in ids]
            break
    if tail:
        tl = [L for L in group_lines(tail) if not re.sub(r"[\s:]+", "", L.text.lower()).startswith(("suggestion", "tip", "note"))
              or len(L.text) > 15]
        if tl:
            tb = min(L.x for L in tl)
            for L in tl:
                starts_new = L.spans[0]["text"].startswith("\uf0fc") or _is_check(L.spans[0]) or L.x <= tb + 2
                if starts_new or not hints:
                    hints.append([None, L.text])
                else:
                    hints[-1][1] = join_wrapped(hints[-1][1], L.text)
    if not spans:
        return steps, hints
    starts = _columns(spans, gap=60)
    lines = []
    for colspans in _split_by_columns(spans, starts):
        cl = [L for L in group_lines(colspans) if not _is_heading_line(L)]
        if cl:
            b = min(L.x for L in cl)
            for L in cl:
                L.base = b
            lines.extend(cl)
    if not lines:
        return steps, hints
    mode = "steps"
    cur = None
    group = None
    for L in lines:
        t = L.text
        base = L.base
        if HINT_HEAD_RE.match(re.sub(r"\s+", "", t.lower()).replace("suggestions", "suggestions")) or \
                re.sub(r"\s+", "", t.lower()) in ("suggestion", "suggestions", "tips", "tip", "note", "notes"):
            mode = "hints"
            cur = None
            continue
        if L.is_label and not re.match(r"^\d", t) and mode == "steps" and len(t) < 40 and \
                not (cur and cur[0] == "hint"):
            group = t.strip("*: ")
            cur = None
            continue
        if not re.search(r"[A-Za-z]", t):
            continue
        m = re.match(r"^(\d{1,2})[.)]?\s+(.*)$", t)
        if mode == "steps" and m and L.x <= base + 3:
            steps.append([group, m.group(2)])
            cur = ("step", len(steps) - 1)
            continue
        if L.text.startswith("") or any(_is_check(s) for s in L.spans[:1]):
            hints.append([None, t])
            cur = ("hint", len(hints) - 1)
            continue
        if HINT_START_RE.match(t) and (L.x <= base + 3 or L.size < 9):
            hints.append([None, t])
            cur = ("hint", len(hints) - 1)
            continue
        if mode == "hints":
            if cur and cur[0] == "hint" and L.x > base + 3:
                hints[cur[1]][1] += " " + t
            elif cur and cur[0] == "hint" and not re.search(r"[.!?]$", hints[cur[1]][1]):
                hints[cur[1]][1] += " " + t
            else:
                hints.append([None, t])
                cur = ("hint", len(hints) - 1)
            continue
        if cur is None:
            steps.append([group, t])
            cur = ("step", len(steps) - 1)
            continue
        lst = steps if cur[0] == "step" else hints
        prev = lst[cur[1]][1]
        lst[cur[1]][1] = join_wrapped(prev, t)
    return steps, hints


NUTR_FIELDS = [
    ("calories", r"calories"), ("protein_g", r"protein"), ("carbohydrates_g", r"(?:total\s+)?carbohydrates?"),
    ("fiber_g", r"(?:dietary\s+)?fib(?:er|re)"), ("sugars", r"(?:total\s+)?sugars?"),
    ("added_sugar_g", r"added\s+sugars?"), ("satfat", r"saturated(?:\s+fat)?"), ("transfat", r"trans\s+fat"), ("fat_g", r"(?:total\s+)?fat"),
    ("cholesterol_mg", r"cholesterol"), ("sodium_mg", r"sodium"), ("potassium_mg", r"potassium"),
    ("phosphorus_mg", r"phosph?or(?:ou|u)s"), ("calcium_mg", r"calcium"), ("iron", r"iron"),
    ("magnesium", r"magnesium"), ("vitc", r"vitamin\s*c"),
]
NUTR_KEYS = ["calories", "protein_g", "carbohydrates_g", "fat_g", "cholesterol_mg", "sodium_mg",
             "potassium_mg", "phosphorus_mg", "calcium_mg", "fiber_g", "added_sugar_g"]
NUTR_RE = re.compile(r"(?<![A-Za-z])(" + "|".join("(?P<%s>%s)" % (k, p) for k, p in NUTR_FIELDS) +
                     r")[ \t]*:?[ \t]*(?P<val>(?:<|less than[ \t]*)?[ \t]*\d[\d,]*(?:\.\d+)?(?![\d/])|trace)?[ \t]*(?P<unit>kcal|mg|g|cal)?\b",
                     re.I)


def parse_nutrients(text):
    """Return (nutrients dict with numeric or None) from free nutrition text."""
    out = {k: None for k in NUTR_KEYS}
    seen = set()
    for m in NUTR_RE.finditer(text):
        key = next(k for k, _ in NUTR_FIELDS if m.group(k))
        val = m.group("val")
        if key not in out or key in seen or not val:
            continue
        seen.add(key)
        v = val.strip().lower()
        if v.startswith("<") or v.startswith("less") or v == "trace":
            continue  # not a plain number; kept in nutrients_raw
        num = float(v.replace(",", ""))
        unit = (m.group("unit") or "").lower()
        if key.endswith("_mg") and unit == "g":
            num *= 1000
        if key.endswith("_g") and unit == "mg":
            num /= 1000
        out[key] = int(num) if num == int(num) else round(num, 2)
    return out


DIET_LABELS = [("ckd non-dialysis", ["CKD non-dialysis"]), ("dialysis/diabetes", ["Dialysis", "Diabetes"]),
               ("dialysis", ["Dialysis"]), ("transplant", [])]


def parse_diets(spans):
    """Diet checkboxes: a visible Wingdings check followed by its label on the same line."""
    found, any_box = [], False
    checks = [s for s in spans if _is_check(s) and not _is_white(s.get("fill"))]
    labels = [s for s in spans if not _is_check(s) and s["text"].strip()]
    for c in checks:
        same = sorted([s for s in labels if s["page"] == c["page"] and abs(s["y"] - c["y"]) < 4
                       and 0 <= s["x"] - c["x2"] < 12], key=lambda s: s["x"])
        if not same:
            continue
        # label text: spans from same line until the next check or gap
        row = sorted([s for s in labels if s["page"] == c["page"] and abs(s["y"] - c["y"]) < 4
                      and s["x"] >= same[0]["x"]], key=lambda s: s["x"])
        txt, last = "", None
        for s in row:
            if last is not None and s["x"] - last > 9:
                break
            nxt_check = [k for k in checks if k["page"] == c["page"] and abs(k["y"] - c["y"]) < 4
                         and same[0]["x"] < k["x"] <= s["x"]]
            if nxt_check:
                break
            txt += s["text"]
            last = s["x2"]
        t = re.sub(r"\s+", " ", txt).strip().lower().rstrip("*")
        for key, vals in DIET_LABELS:
            if t.startswith(key):
                any_box = True
                for v in vals:
                    if v not in found:
                        found.append(v)
                break
    return found, any_box


def smart_title(t):
    t = fix_text(t)
    small = {"and", "with", "of", "in", "on", "a", "an", "the", "or", "for", "to", "en"}
    words = t.lower().split()
    out = []
    for i, w in enumerate(words):
        if i and w in small:
            out.append(w)
        else:
            out.append("-".join(p[:1].upper() + p[1:] for p in w.split("-")))
    return " ".join(out).replace("’S", "’s").replace("'S", "'s")


def parse_times(text):
    res = {"prep_time": None, "cook_time": None, "total_time": None, "portions": None, "extra": []}
    for part in re.split(r"\s*\|\s*|\s{2,}|\n", text):
        p = part.strip()
        m = re.match(r"^(PREP(?:ARATION)?(?: TIME)?)\s*:\s*(.+)$", p, re.I)
        if m:
            res["prep_time"] = m.group(2).strip().lower()
            continue
        m = re.match(r"^((?:COOKING|COOK|BAKING|BAKE|GRILLING|ROASTING)(?: TIME)?)\s*:\s*(.+)$", p, re.I)
        if m:
            res["cook_time"] = m.group(2).strip().lower()
            continue
        m = re.match(r"^TOTAL(?: TIME)?\s*:\s*(.+)$", p, re.I)
        if m:
            res["total_time"] = m.group(1).strip().lower()
            continue
        m = re.match(r"^(SERVINGS?|MAKES|YIELDS?)\s*:?\s*(.+)$", p, re.I)
        if m:
            v = m.group(2).strip()
            res["portions"] = v if re.match(r"^\d+$", v) else v.lower()
            continue
        if re.match(r"^[A-Z ]+:\s*\d", p):
            res["extra"].append(p)
            continue
        if re.match(r"^\d[\d /]*\s+[A-Za-z]", p) and not re.search(r"minute|hour", p, re.I) and not res["portions"]:
            res["portions"] = p.lower()
    return res


def parse_pdf_recipe(data):
    spans, images = pdf_extract(data)
    spans = [s for s in spans if s["size"] >= 3.9 and -5 < s["y"] and s["rot"] == 0]
    pages = sorted(set(s["page"] for s in spans))
    by_page = {p: group_lines([s for s in spans if s["page"] == p]) for p in pages}
    rec = {"ingredients": [], "steps": [], "hints": [], "nutrients_raw": None, "serving_size": None,
           "food_choices": [], "diet": [], "title_pdf": None}

    # title: largest text on the first page
    if pages:
        p0 = [L for L in by_page[pages[0]] if L.size >= 18]
        if p0:
            mx = max(L.size for L in p0)
            tl = [L for L in p0 if L.size >= mx - 2]
            rec["title_pdf"] = " ".join(L.text for L in tl)

    # times / servings line(s)
    tlines = []
    for p in pages:
        for L in by_page[p]:
            if (re.search(r"\b(PREPARATION|PREP|COOKING|BAKING|SERVINGS?|MAKES|SOAKING|RESTING|CHILLING|FREEZING)\s*:?\s*\d|"
                          r"\bSERVINGS?:|\bMAKES\b", L.text) or
                re.match(r"^\d[\d /]*\s+[A-Z][A-Z0-9 -]+$", L.text) and not re.search(r"MINUTE|HOUR", L.text)) \
                    and L.text.upper() == L.text and len(L.text) < 120:
                tlines.append(" | ".join(t for _, _, _, t in line_segments(L.spans)))
        if tlines:
            break
    rec["times"] = parse_times(" | ".join(tlines))

    spans_by_page = {p: [s for s in spans if s["page"] == p] for p in pages}
    ih = _heading(spans_by_page, "ingredients")
    rec["description"] = None
    if ih:
        dl = [L for L in group_lines([s for s in strip_footer(spans_by_page[ih[0]]) if s["y"] > ih[2] + 6
                                      and 7.5 <= s["size"] < 14])]
        dl = [L for L in dl if not re.search(r"\b(PREPARATION|SERVINGS?|COOKING|MAKES)\b", L.text)
              and not re.search(r"\bCHECK\b", L.text)]
        if dl:
            d = fix_text(" ".join(L.text for L in dl))
            rec["description"] = d if len(re.findall(r"[A-Za-z]{2,}", d)) >= 6 else None
    ph = _heading(spans_by_page, "preparation") or _heading(spans_by_page, "directions") or \
        _heading(spans_by_page, "instructions")
    if ih and ph and ih[0] == ph[0]:
        pno = ih[0]
        page_spans = strip_footer([s for s in spans if s["page"] == pno])
        notes_spans = []
        if ph[1] > ih[1] + 60:   # side by side columns
            bound = ph[1] - 6
            # full-width paragraphs crossing the column boundary are notes
            for line in _raw_lines([s for s in page_spans if s["y"] < min(ih[2], ph[2]) - 2 and s["x"] >= ih[1] - 8]):
                for g in segment_groups(line):
                    straddle = any(x["x"] < ph[1] - 3 and x["x2"] > ph[1] + 3 and x["text"].strip() for x in g)
                    if min(x["x"] for x in g) < bound - 20 and max(x["x2"] for x in g) > bound + 20 and straddle:
                        notes_spans.extend(g)
            if notes_spans:   # everything below the first full-width line belongs to the note
                y0 = max(x["y"] for x in notes_spans) + 1
                notes_spans = [x for x in page_spans if x["y"] <= y0 and x["x"] >= ih[1] - 8]
            ids = set(id(x) for x in notes_spans)
            page_spans = [s for s in page_spans if id(s) not in ids]
            ing = [s for s in page_spans if ih[1] - 8 <= s["x"] < bound and s["y"] < ih[2] + 6]
            prep = [s for s in page_spans if s["x"] >= bound and s["y"] < ph[2] + 6]
        else:                         # stacked
            top, bot = (ih, ph) if ih[2] > ph[2] else (ph, ih)
            a = [s for s in page_spans if s["x"] >= top[1] - 8 and bot[2] + 2 < s["y"] < top[2] + 6]
            b = [s for s in page_spans if s["x"] >= bot[1] - 8 and s["y"] < bot[2] + 6]
            ing, prep = (a, b) if top is ih else (b, a)
        # drop footer lines
        ing = [s for s in ing if not FOOTER_RE.search(s["text"])]
        prep = [s for s in prep if not FOOTER_RE.search(s["text"])]
        rec["ingredients"], h1 = parse_ingredient_region(ing)
        rec["steps"], h2 = parse_prep_region(prep)
        rec["hints"] = h1 + h2
        if notes_spans:
            nt = fix_text(" ".join(L.text for L in group_lines(notes_spans)))
            if nt:
                rec["hints"].append([None, nt])

    # nutrition block
    nh = None
    for p in pages:
        for L in by_page[p]:
            sp0 = [x for x in L.spans if x["text"].strip()]
            if re.sub(r"\s+", "", L.text.lower()).startswith("perserving") and sp0 and sp0[0]["size"] < 8:
                nh = (p, sp0[0]["x"], L.y, sp0[0]["size"])
                break
        if nh:
            break
    if nh:
        p, nx, ny = nh[:3]
        ns = nh[3]
        pg = strip_footer(spans_by_page[p])
        nspans = [s for s in pg if s["y"] <= ny + 1 and nx - 70 <= s["x"] <= nx + 200 and s["size"] <= ns + 0.3]
        note_spans = [s for s in pg if s["y"] < ny and nx + 80 <= s["x"] <= nx + 300 and ns + 0.3 < s["size"] < 6.9]
        nl = group_lines(nspans)
        raw = []
        for L in nl:
            t = " ".join(tt for _, _, _, tt in line_segments(L.spans, colgap=3))
            if re.match(r"^diet\s*types", t, re.I):
                continue
            t = re.sub(r"\s*(CKD Non-)?Dialy\w*(/Diabet\w*)?\s*\*?|\s*T\s?ransplant\w*|\s+T$", " ", t).strip()
            if t:
                raw.append(t)
        txt = "\n".join(raw)
        rec["nutrients_raw"] = fix_text(txt.replace("\n", "; "))
        rec["nutrients"] = parse_nutrients(txt)
        m = re.search(r"per\s*ser\s*ving\s*:?\s*(.*?)\s*(?:renal|$)", txt.replace("\n", " "), re.I | re.S)
        if m and m.group(1).strip():
            rec["serving_size"] = fix_text(m.group(1)).strip(" :")
        m = re.search(r"exchanges?\s*:?\s*(.*?)\s*calories", txt.replace("\n", " "), re.I | re.S)
        if m:
            ex = fix_text(m.group(1))
            rec["food_choices"] = [x.strip() for x in re.split(r"\s*\+\s*", ex) if x.strip()]
        # notes inside the nutrition area (e.g. "PLEASE NOTE: ...")
        if note_spans:
            nt = fix_text(" ".join(L.text for L in group_lines(note_spans)))
            if nt:
                rec["hints"].append([None, nt])
        # starred footnotes under the nutrients ("*Can be lower with soaking", "* 1/2 serving if not main meal")
        small = [x for x in strip_footer(spans_by_page[p]) if x["y"] < ny and x["size"] <= 6]
        for L in group_lines(small):
            if L.text.startswith("*"):
                fx, fy = L.x, L.y
                cont = [x for x in small if x["y"] < fy - 1 and fx - 1 <= x["x"] < fx + 160]
                txt, last = L.text, fy
                for C in group_lines(cont):
                    if C.text.startswith("*") or last - C.y > 12:
                        break
                    txt = join_wrapped(txt, C.text)
                    last = C.y
                rec["hints"].append([None, fix_text(txt)])
    else:
        rec["nutrients"] = {k: None for k in NUTR_KEYS}

    # side article ("POTASSIUM CHECK" / "PHOSPHORUS CHECK" / "NUTRITION CHECK")
    for p in pages:
        chk = None
        for line in _raw_lines(spans_by_page[p]):
            for g in segment_groups(line):
                g = [x for x in g if x["size"] < 20]
                t = re.sub(r"\s+", "", "".join(x["text"] for x in g))
                m = re.search(r"([A-Z]+CHECK)", t)
                if m:
                    cx = _find_word_x(g, m.group(1).lower())
                    if cx is not None and cx > 200:
                        chk = (cx, max(x["y"] for x in g))
                        break
            if chk:
                break
        if not chk:
            continue
        ax, cy = chk
        art_spans = [s for s in strip_footer(spans_by_page[p]) if s["x"] >= ax - 5 and s["y"] < cy - 2
                     and s["size"] >= 7.5]
        alines = group_lines(art_spans)
        heading, paras, last_y, body_size = [], [], None, None
        for L in alines:
            if L.size >= 12:
                if paras:
                    break
                heading.append(L.text)
                continue
            if last_y is not None and last_y - L.y > L.size * 1.75:
                paras.append("")
            if not paras:
                paras.append("")
            paras[-1] = (paras[-1] + (" " if paras[-1] and not paras[-1].endswith("-") else "") + L.text)
            last_y = L.y
        label = fix_text(" ".join(heading)) or None
        body = [fix_text(x) for x in paras if x.strip()]
        if body:
            rec["hints"].append([label, "\n\n".join(body)])
        break

    rec["diet"], rec["diet_boxes"] = parse_diets(spans)

    # photo: largest JPEG image
    jpgs = [im for im in images if im.get("raw") and im.get("w") and im.get("h")]
    jpgs.sort(key=lambda im: im["w"] * im["h"], reverse=True)
    rec["image"] = jpgs[0] if jpgs else None
    return rec


# ---------------------------------------------------------------------------
# HTML recipe posts (category "Recipe")
# ---------------------------------------------------------------------------
from html.parser import HTMLParser


class BlockParser(HTMLParser):
    """Flatten HTML into (tag, text, div_class_path) blocks for h1-h6 / p / li."""
    BLOCKS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.buf, self.cur, self.divs = [], [], None, []

    def flush(self):
        if self.cur is not None:
            t = re.sub(r"\s+", " ", "".join(self.buf)).strip()
            if t:
                self.blocks.append((self.cur, t, " ".join(self.divs)))
        self.buf, self.cur = [], None

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            self.divs.append(dict(attrs).get("class", ""))
        if tag in self.BLOCKS:
            self.flush()
            self.cur = tag
        elif tag == "br" and self.cur is not None:
            self.buf.append("\n")

    def handle_endtag(self, tag):
        if tag in self.BLOCKS:
            self.flush()
        if tag == "div":
            self.flush()
            if self.divs:
                self.divs.pop()

    def handle_data(self, data):
        if self.cur is None:
            if data.strip():
                self.cur = "p"
            else:
                return
        self.buf.append(data)


ATTRIB_RE = re.compile(r"originally appeared|copyright|all rights reserved|reprinted|courtesy of|^source:|sponsor|"
                       r"contributed by|contibuted by|^kidney friendly recipes$", re.I)
HTML_HINT_RE = re.compile(r"^(suggestions?|tips?|notes?|helpful hints?|for those with|variation|leaching)", re.I)


def parse_html_post(url, page):
    title_m = re.search(r'<h1 class="entry-title">(.*?)</h1>', page, re.S)
    title = clean_text(title_m.group(1)) if title_m else None
    img = None
    m = re.search(r'<img[^>]+class="[^"]*wp-post-image[^"]*"[^>]*>', page)
    if m:
        src = re.search(r'\bsrc="([^"]+)"', m.group(0))
        img = urljoin(url, htmlmod.unescape(src.group(1))) if src else None
    seg = page[page.find('class="entry-content'):]
    seg = seg[:seg.find('<footer class="entry-footer')] if '<footer class="entry-footer' in seg else seg
    bp = BlockParser()
    bp.feed(seg[seg.find(">") + 1:])
    bp.flush()
    rec = {"title": title, "image_url": img, "ingredients": [], "steps": [], "hints": [], "nutrients_raw": None,
           "serving_size": None, "food_choices": [], "carb_choices": None, "portions": None, "description": None}
    section, nut_lines, group, sub = None, [], None, None
    for tag, text, divs in bp.blocks:
        t = fix_text(text)
        low = t.lower().rstrip(":")
        if tag.startswith("h"):
            if "ingredient" in low:
                section = "ing"
            elif "nutrition" in low or "nutrient" in low:
                section = "nut"
            elif low == "diet":
                section = "diet"
            elif "direction" in low or "preparation" in low or "instruction" in low:
                section, group = "dir", None
            else:
                section = "other"
            sub = None
            continue
        if "pos-bottom" in divs:
            section = "bottom"
        if ATTRIB_RE.search(t):
            continue
        if section == "ing":
            if t.endswith(":") and not re.match(r"^[\d¼½¾⅓⅔⅛]", t):
                group = t.rstrip(":")
                continue
            rec["ingredients"].append([group, t.lstrip("•· ").strip()])
        elif section == "nut":
            if re.match(r"^per serving", t, re.I):
                rec["serving_size"] = re.sub(r"^per serving\s*:?\s*", "", t, flags=re.I).strip(" ()") or None
                m2 = re.match(r"^(1/(\d+))\s+of\s+recipe", rec["serving_size"] or "")
                if m2:
                    rec["portions"] = m2.group(2)
                continue
            m2 = re.match(r"^1 serving\s*=\s*(.+)$", t, re.I)
            if m2:
                rec["serving_size"] = m2.group(1).strip()
                continue
            m2 = re.match(r"^renal(?: and renal diabetic)? exchanges?\s*:\s*(.+)$", t, re.I)
            if m2:
                rec["food_choices"] = [x.strip() for x in re.split(r"\s*\+\s*", m2.group(1)) if x.strip()]
                continue
            if re.match(r"^renal(?: and renal diabetic)? food choices?$", t, re.I):
                sub = "fc"
                continue
            if re.match(r"^carbohydrate choices?$", t, re.I):
                sub = "cc"
                continue
            if sub == "fc" and tag == "li":
                rec["food_choices"].append(t)
                continue
            if sub == "cc" and tag == "li":
                rec["carb_choices"] = t
                continue
            if not re.search(r"\d", t) and re.match(r"^\d", t) is None and tag == "p" and len(t) > 60:
                rec["hints"].append([None, t])
                continue
            if re.match(r"^\d+\s+[A-Za-z]", t) and not re.search(r"\d\s*(g|mg|kcal|calories)\b", t, re.I):
                # exchange list written as separate lines ("1 Starch", "1 Fat")
                rec["food_choices"].append(t)
                continue
            nut_lines.append(t)
        elif section == "dir":
            if HTML_HINT_RE.match(t) and rec["steps"]:
                rec["hints"].append([None, t])
                continue
            if tag == "p" and t.endswith(":") and len(t) < 50:
                if low in ("preparation",):
                    continue
                group = t.rstrip(":")
                continue
            rec["steps"].append([group, re.sub(r"^preparation:\s*", "", t, flags=re.I)])
        elif section == "bottom" or section == "other":
            if re.match(r"^helpful hints?$", low):
                sub = "hints"
                continue
            rec["hints"].append([None, re.sub(r"^(suggestions?|tips?)\s*:\s*", "", t, flags=re.I)
                                 if False else t])
    raw = "; ".join(nut_lines)
    rec["nutrients_raw"] = raw or None
    norm = re.sub(r"\bmilligrams?\b", "mg", raw, flags=re.I)
    norm = re.sub(r"\bgrams?\b", "g", norm, flags=re.I)
    norm = re.sub(r"(\d)\s*calories\b", r"\1 kcal", norm, flags=re.I)
    sections = re.split(r"(?i)nutrient analysis\s*:[^;]*;", norm)
    sections = [x for x in sections if x.strip(" ;")]
    if len(sections) > 1:
        # analysis given per component (e.g. "Beef Mixture" + "Pasta"): the serving is their sum
        parts = [parse_nutrients(x.replace("; ", "\n")) for x in sections]
        rec["nutrients"] = {k: (round(sum(p[k] for p in parts), 2) if all(p[k] is not None for p in parts) else None)
                            for k in NUTR_KEYS}
        rec["hints"].append([None, "Nutrient values are the sum of the separate analyses given for each component."])
    else:
        rec["nutrients"] = parse_nutrients(norm.replace("; ", "\n"))
    rec["steps"] = [s for s in rec["steps"] if s[1]]
    return rec


# ---------------------------------------------------------------------------
# Children's National cookbook PDF (18 recipes, rotated pages)
# ---------------------------------------------------------------------------
COOKBOOK_URL = "https://aakp.org/wp-content/uploads/2020/09/73644-Childrens-National-Cookbook-Proof-13-2.pdf"
CUISINE_MAP = [("mexic", ["Mexican"]), ("india", ["Indian"]), ("middle east", ["Middle Eastern"]),
               ("bahama", ["Caribbean"]), ("german", ["German"]), ("ital", ["Italian"]),
               ("southeastern usa", ["Southern", "American"]), ("usa", ["American"]),
               ("south american/asian", ["South American", "Asian"]), ("nepal", ["Asian"]),
               ("tibet", ["Asian"])]


def _fix_stacked_fractions(spans):
    """Cookbook writes 1/3 as a small raised '1', a span starting with '/', and sometimes a lowered '3'."""
    spans = sorted(spans, key=lambda s: (s["x"], -s["y"]))
    used = set()
    for s in spans:
        if not s["text"].startswith("/"):
            continue
        for o in spans:
            if id(o) in used or o is s or not re.fullmatch(r"\d", o["text"].strip()):
                continue
            if o["size"] < s["size"] * 0.85 and abs(o["y"] - s["y"]) < 10:
                if abs(o["x2"] - s["x"]) < 2.5 and o["x"] < s["x"]:
                    s["text"] = o["text"].strip() + s["text"]
                    s["x"] = o["x"]
                    used.add(id(o))
                elif 0 <= o["x"] - s["x"] < 8 and o["y"] < s["y"]:
                    s["text"] = s["text"][:s["text"].index("/") + 1] + o["text"].strip() + s["text"][s["text"].index("/") + 1:]
                    used.add(id(o))
    return [s for s in spans if id(s) not in used]


def parse_cookbook(data):
    spans, images = pdf_extract(data)
    spans = [s for s in spans if s["size"] >= 3.9]
    toc = {}
    out = []
    for p in sorted(set(s["page"] for s in spans)):
        ps = _fix_stacked_fractions([s for s in spans if s["page"] == p])
        lines = group_lines(ps)
        for L in lines:
            m = re.match(r"^(.+?)\.{3,}\s*(.+?)\.{3,}\s*(.+?)\.{3,}\s*(\d+)$", L.text)
            if m:
                toc[slugify(m.group(1))] = {"title": m.group(1).strip(), "type": m.group(2), "region": m.group(3)}
        heads = []
        for line in _raw_lines(ps):
            t = re.sub(r"\s+", "", "".join(x["text"] for x in sorted(line, key=lambda x: x["x"]))).lower()
            if t == "ingredientsdirections":
                heads.append((max(x["y"] for x in line), _find_word_x(line, "directions")))
        heads.sort(key=lambda h: -h[0])
        for i, (hy, dx) in enumerate(heads):
            lower = heads[i + 1][0] if i + 1 < len(heads) else -1e9
            # title block: the 24pt line and the "Serves" line just above the heading
            above = [L for L in lines if hy < L.y < hy + 95]
            tl = [L for L in above if L.size >= 20]
            if not tl:
                continue
            tline = tl[-1]
            tspans = sorted([s for s in tline.spans if s["text"].strip()], key=lambda s: s["x"])
            tfont = tspans[0]["font"]
            title = fix_text(" ".join(t for _, _, _, t in line_segments([s for s in tspans if s["font"] == tfont])))
            subtitle = fix_text(" ".join(t for _, _, _, t in line_segments([s for s in tspans if s["font"] != tfont])))
            serves = " ".join(L.text for L in above if L.y < tline.y and L.size < 20)
            # next recipe's title block starts ~ 75pt above its heading
            block = [s for s in ps if lower + 95 < s["y"] < hy - 2 and not (s["x"] > 600 and re.fullmatch(r"\d{1,2}", s["text"].strip()))]
            nut_i = nut_x = None
            for line in _raw_lines(block):
                tx = "".join(x["text"] for x in line)
                if "NUTRITION" in tx:
                    nut_i = max(x["y"] for x in line) + 1
                    nut_x = _find_word_x(line, "nutrition")
                    break
            nut = [s for s in block if nut_i is not None and s["y"] <= nut_i and s["x"] >= nut_x - 2]
            ids = set(id(x) for x in nut)
            body = [s for s in block if id(s) not in ids]
            ing, prep = [], []
            for line in _raw_lines(body):
                for g in segment_groups(line):
                    (ing if min(x["x"] for x in g) < dx - 6 else prep).extend(g)
            ingredients, h1 = parse_ingredient_region(ing)
            # all-caps labels such as "FOR STEW:" / "OPTIONAL FLAVORINGS:"
            ingredients2, group = [], None
            for g, t in ingredients:
                mm = re.match(r"^([A-Z][A-Z ()]+):\s*(.*)$", t)
                if mm and mm.group(1).upper() == mm.group(1):
                    group = mm.group(1).title()
                    if mm.group(2):
                        ingredients2.append([group, mm.group(2)])
                    continue
                ingredients2.append([g or group, t])
            steps, h2 = parse_prep_region(prep)
            steps2 = []
            for g, t in steps:
                mm = re.match(r"^([A-Z][A-Z ()]+):\s*(.+)$", t)
                if mm:
                    steps2.append([None, t])
                else:
                    steps2.append([g, t])
            note_sp = [x for x in nut if x["size"] <= 10.5]
            nraw = fix_text(" ".join(L.text for L in group_lines(nut)))
            nut = [x for x in nut if x["size"] > 10.5]
            first = re.split(r"\b(?:WITH [A-Z ,]+:)", fix_text(" ".join(L.text for L in group_lines(nut))))[0]
            if note_sp:
                nt = fix_text(" ".join(L.text for L in group_lines(note_sp)))
                if len(re.findall(r"[A-Za-z]{2,}", nt)) >= 3 and not nt.endswith(":"):
                    h2 = h2 + [[None, nt]]
            nutr = {k: None for k in NUTR_KEYS}
            vals = re.findall(r"(\d+(?:\.\d+)?)\s*(mg|g)?\s*(calories|protein|phosphorus|sodium|potassium)", first, re.I)
            if len(vals) >= 3 and not re.search(r"NUTRITION[^:]*:\s*(?:\([^)]*\)\s*)?calories\b", first, re.I):
                key = {"calories": "calories", "protein": "protein_g", "phosphorus": "phosphorus_mg",
                       "sodium": "sodium_mg", "potassium": "potassium_mg"}
                for v, _, k in vals:
                    kk = key[k.lower()]
                    if nutr[kk] is None:
                        num = float(v)
                        nutr[kk] = int(num) if num == int(num) else num
            else:
                nutr = parse_nutrients(first)
            # page photo (only when the page holds a single recipe)
            pimgs = [im for im in images if im["page"] == p and (im.get("w") or 0) >= 500]
            meta = toc.get(slugify(title), {})
            out.append({
                "title": title, "subtitle": subtitle or None, "page": p, "serves": serves,
                "ingredients": ingredients2, "steps": steps2, "hints": h1 + h2,
                "nutrients": nutr, "nutrients_raw": nraw or None, "toc": meta,
                "images": pimgs if len(heads) == 1 else [],
            })
    return out, toc


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------
DISH_TYPE_RULES = [  # checked in order; first match wins
    ("Desserts", r"(?<!fish )\bcakes?\b|cupcake|cookie|crackles|custard|key lime|tiramisu|sorbet|sherbet|granita|"
                 r"ice cream|cheesecake|crumble|cobbler|crostata|cream puff|pudding|parfait|eton mess|semifreddo|"
                 r"lemon square|crispy treats|mango lime cream|cinnamon cream|grilled pineapple|bundle|brownie|"
                 r"^(?!.*(meat|shepherd|pot pie|noodle|onion|chicken|turkey)).*\bpies?\b|dessert|souffl"),
    ("Beverages", r"smoothie|\bdrink\b|mocktail|coffee|lemonade|\btea\b|\batol\b|punch|shake|beverage|nepro"),
    ("Breakfast & Brunch", r"pancake|waffle|omelet|omelette|frittata|quiche|oatmeal|\boats\b|french toast|breakfast|"
                           r"strata|shakshuka|baked eggs|egg white|biscuits"),
    ("Soups & Stews", r"\bsoup\b|\bstew\b|\bchili\b(?!-lime)|margog"),
    ("Salads & Dressings", r"salad|slaw"),
    ("Sauces & Seasonings", r"^(?!.*\bwith\b).*(\bsauce\b|dressing|seasoning|spice mix|mayonnaise|chutney|salsa)"),
    ("Appetizers & Snacks", r"\bdip\b|rillettes|spring rolls|snack|bites|cucumber cups|momos|dumpling|crisps|chips|"
                            r"spread"),
    ("Pizza & Sandwiches", r"pizza|sandwich|burger|slider|\bwraps?\b|pockets|grilled cheese|sloppy joe|crab rolls|"
                           r"english muffin|souvlaki"),
    ("Breads", r"muffin|\bloaf\b|bread|scone|biscuit|bagel"),
]
MAIN_RULES = [
    ("Fish & Seafood", r"\bfish|salmon|tuna|shrimp|\bcrab|tilapia|\bcod\b|seafood|scallop|prawn"),
    ("Chicken & Turkey", r"chicken|turkey|poultry|pollo"),
    ("Beef, Lamb & Pork", r"\bbeef|steak|\bpork|\blamb\b|meatloaf|meat loaf|meatball|\bribs\b|kofta|sausage|"
                          r"hamburger|short rib|carne|\bveal"),
    ("Pasta, Rice & Grains", r"pasta|penne|rotini|linguin|farfalle|orzo|couscous|risotto|\brice\b|noodle|barley|"
                             r"bulgur|pilaf|pulao|lasagna|quinoa|vermicelli|spaghetti|macaroni|\bgrains?\b|buddha"),
]
VEG_RULE = (r"\b(vegetables?|vegetarian|tofu|eggplant|peppers?|zucchini|cabbage|beans?|lentils?|chickpeas?|fries|"
            r"mushrooms?|cauliflower|chop suey|mock meat|potato(es)?|asparagus|squash|carrots?|burrito|enchiladas?)\b")


def classify(title, ingredients):
    t = title.lower()
    for cat, rx in DISH_TYPE_RULES:
        if re.search(rx, t):
            return cat
    best = None
    for cat, rx in MAIN_RULES:
        m = re.search(rx, t)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), cat)
    if best:
        return best[1]
    if re.search(VEG_RULE, t):
        return "Vegetables"
    ing = " ".join(x for _, x in ingredients).lower()
    for cat, rx in MAIN_RULES[:3]:
        if re.search(rx, ing):
            return cat
    return "Vegetables"


CUISINE_RULES = [
    ("Mexican", r"mexic|burrito|taco|enchilada|fajita|tostada|quesadilla|salsa"),
    ("Italian", r"italian|risotto|pesto|lasagna|tiramisu|marinara|primavera|scaloppin|semifreddo|spaghetti|penne|"
                r"rotini|linguin|farfalle|frittata"),
    ("Asian", r"asian|stir.fry|soba|sesame|spring roll|hoisin|teriyaki|general tao|chop suey|momos|tibet|nepal"),
    ("Chinese", r"chinese|fried rice|chop suey|general tao"),
    ("Japanese", r"japanese|mirin|teriyaki"),
    ("Hawaiian", r"poke bowl|hawaii"),
    ("Indian", r"india|tandoori|curr(y|ied)|pulao|masala|naan"),
    ("Greek", r"greek|souvlaki|tzatziki"),
    ("Middle Eastern", r"middle east|kofta|shakshuka|harissa|margog|hummus|falafel"),
    ("Mediterranean", r"mediterranean|provencal|provençal"),
    ("French", r"provencal|provençal|rillettes|souffl|quiche"),
    ("Caribbean", r"caribbean|bahamian|jerk"),
    ("South American", r"peruvian|south american|solterito"),
    ("Southern", r"southern|kentucky|creole|cajun"),
    ("German", r"german"),
    ("Thai", r"\bthai\b"),
]
ALLOWED_CUISINE = {"American", "Asian", "Caribbean", "Chinese", "Filipino", "French", "German", "Greek", "Hawaiian",
                   "Indian", "Irish", "Italian", "Japanese", "Jewish", "Mediterranean", "Mexican", "Middle Eastern",
                   "Native American", "South American", "Southern"}


def infer_cuisine(text):
    t = text.lower()
    out = []
    for c, rx in CUISINE_RULES:
        if c in ALLOWED_CUISINE and re.search(rx, t) and c not in out:
            out.append(c)
    if re.search(r"\bthai\b", t):
        out = [c for c in out if c != "Indian"]
        if "Asian" not in out:
            out.append("Asian")
    return out


def infer_method(steps_text, title):
    t = (title + " " + steps_text).lower()
    out = []
    if re.search(r"slow cooker|crock.?pot", t):
        out.append("Slow Cooker")
    if re.search(r"\bbake|baking|baked\b", t):
        out.append("Bake")
    if re.search(r"\boven\b|broil", t):
        out.append("Oven")
    if re.search(r"\broast", t):
        out.append("Roast")
    if re.search(r"\bgrill", t):
        out.append("Grill")
    if re.search(r"microwave", t):
        out.append("Microwave")
    if re.search(r"\bfr(y|ied|ying)\b", t):
        out.append("Fry")
    if re.search(r"skillet|saucepan|frying pan|stock ?pot|\bwok\b|stove|simmer|boil|saut[eé]|medium heat|"
                 r"high heat|low heat", t):
        out.append("Stove Top")
    if not out and not re.search(r"heat|cook|toast|warm", t):
        out.append("No Cooking")
    return out


def infer_dish(title, category, ingredients, steps_text):
    t = title.lower()
    out = []
    pairs = [("Soup", r"\bsoup\b"), ("Stew", r"\bstew\b|\bchili\b(?!-lime)"), ("Stir-fry", r"stir.?fry"),
             ("Cookies", r"cookie|crackles"), ("Cake", r"(?<!fish )\bcakes?\b|cupcake|cheesecake"),
             ("Pie", r"\bpies?\b|tart\b"), ("Muffin", r"muffin"),
             ("Bread", r"\bbread\b(?! pudding)|\bloaf\b|biscuit"), ("Candy", r"candy|fudge")]
    for d, rx in pairs:
        if re.search(rx, t):
            out.append(d)
    if re.search(r"slow cooker|one.pot|sheet pan|skillet casserole", (t + " " + steps_text.lower())) and \
            category not in ("Desserts", "Beverages"):
        if re.search(r"one.pot|sheet pan|skillet casserole|slow cooker", t):
            out.append("One-Dish Meal")
    if 0 < len(ingredients) <= 5:
        out.append("5 or less ingredients")
    return out


def portions_from_serving(ss):
    if not ss:
        return None
    m = re.match(r"^\s*(?:1/(\d+)|⅛|¼|½|⅓|⅙)\s+of\s+(?:the\s+)?recipe", ss)
    if m:
        if m.group(1):
            return m.group(1)
        return {"⅛": "8", "¼": "4", "½": "2", "⅓": "3", "⅙": "6"}[ss.strip()[0]]
    return None


def dedupe_hints(hints):
    out = []
    for g, t in hints:
        t = (t or "").strip()
        if not t or not re.search(r"[A-Za-z]{3}", t):
            continue
        k = re.sub(r"\W+", "", t.lower())
        dup = False
        for i, (g2, t2) in enumerate(out):
            k2 = re.sub(r"\W+", "", t2.lower())
            if k in k2:
                dup = True
                break
            if k2 in k:
                out[i] = [g or g2, t]
                dup = True
                break
        if not dup:
            out.append([g, t])
    return out


def empty_record():
    return {
        "source": KEY, "source_name": SOURCE_NAME, "source_id": None, "url": None, "lang": "en", "title": None,
        "description": None, "image_url": None, "image_path": None, "portions": None, "serving_size": None,
        "category": None, "diet": [], "dish": [], "cuisine": [], "method": [],
        "nutrients": {k: None for k in NUTR_KEYS}, "nutrients_raw": None, "ingredients": [], "steps": [],
        "hints": [], "food_choices": [], "carb_choices": None, "video_url": None, "prep_time": None,
        "cook_time": None, "total_time": None, "translation_of": None,
    }


def finish_record(r):
    r["hints"] = dedupe_hints(r["hints"])
    r["ingredients"] = [[g, fix_text(t)] for g, t in r["ingredients"] if fix_text(t)]
    r["steps"] = [[g, fix_text(t)] for g, t in r["steps"] if fix_text(t)]
    steps_text = " ".join(t for _, t in r["steps"])
    r["category"] = classify(r["title"], r["ingredients"])
    r["method"] = infer_method(steps_text, r["title"])
    if not r["cuisine"]:
        r["cuisine"] = infer_cuisine(r["title"] + " " + (r["description"] or ""))
    r["dish"] = infer_dish(r["title"], r["category"], r["ingredients"], steps_text)
    return r


def title_tokens(t):
    stop = {"and", "with", "the", "a", "of", "in", "on", "for", "or"}
    return set(w for w in re.findall(r"[a-z]+", t.lower()) if w not in stop)


def titles_match(a, b):
    ta, tb = title_tokens(a), title_tokens(b)
    if not ta or not tb:
        return True
    return len(ta & tb) / float(min(len(ta), len(tb))) >= 0.5


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------


def invert_jpeg_coefficients(data):
    """Losslessly negate every DCT coefficient of a baseline JPEG (all components).
    Used for CMYK/YCCK photos embedded in PDFs without the Adobe inversion: after this,
    viewers that apply the Adobe CMYK convention show the right colours. Returns None if unsupported."""
    pos = 2
    out = bytearray(data[:2])
    huff = {}
    comps = {}
    order = []
    dri = 0
    while pos < len(data):
        if data[pos] != 0xFF:
            return None
        m = data[pos + 1]
        if m == 0xD9:
            out += data[pos:pos + 2]
            break
        L = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        seg = data[pos:pos + 2 + L]
        if m in (0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            return None  # only baseline huffman supported
        if m == 0xC0:
            nc = seg[9]
            height, width = struct.unpack(">HH", seg[5:9])
            order = []
            for k in range(nc):
                cid, hv, tq = seg[10 + 3 * k], seg[11 + 3 * k], seg[12 + 3 * k]
                comps[cid] = (hv >> 4, hv & 15)
                order.append(cid)
        elif m == 0xC4:
            q = 4
            while q < len(seg):
                tc_th = seg[q]
                counts = seg[q + 1:q + 17]
                n = sum(counts)
                syms = seg[q + 17:q + 17 + n]
                # 16-bit lookup: value -> (length, symbol)
                lut = [None] * 65536
                code, k = 0, 0
                for ln in range(1, 17):
                    for _ in range(counts[ln - 1]):
                        base = code << (16 - ln)
                        for v in range(base, base + (1 << (16 - ln))):
                            lut[v] = (ln, syms[k])
                        k += 1
                        code += 1
                    code <<= 1
                huff[(tc_th >> 4, tc_th & 15)] = lut
                q += 17 + n
        elif m == 0xDD:
            dri = struct.unpack(">H", seg[4:6])[0]
        elif m == 0xDA:
            ns = seg[4]
            scomp = []
            for k in range(ns):
                cid, t = seg[5 + 2 * k], seg[6 + 2 * k]
                scomp.append((cid, t >> 4, t & 15))
            if seg[5 + 2 * ns] != 0 or seg[6 + 2 * ns] != 63 or seg[7 + 2 * ns] != 0:
                return None
            out += seg
            pos += 2 + L
            # entropy-coded data up to next non-RST marker
            end = pos
            while True:
                end = data.find(b"\xff", end)
                if end < 0:
                    return None
                nb = data[end + 1]
                if nb == 0x00 or 0xD0 <= nb <= 0xD7:
                    end += 2
                    continue
                break
            ecs = data[pos:end]
            try:
                res = _transcode_scan(ecs, scomp, comps, huff, dri, width, height)
            except (IndexError, KeyError, TypeError):
                return None
            if res is None:
                return None
            out += res
            pos = end
            continue
        out += seg
        pos += 2 + L
    return bytes(out)


def _transcode_scan(ecs, scomp, comps, huff, dri, width, height):
    # split into restart intervals
    parts = []
    i, start = 0, 0
    while True:
        j = ecs.find(b"\xff", i)
        if j < 0:
            parts.append((ecs[start:], None))
            break
        nb = ecs[j + 1]
        if 0xD0 <= nb <= 0xD7:
            parts.append((ecs[start:j], ecs[j:j + 2]))
            start = i = j + 2
        else:
            i = j + 2
    hmax = max(comps[c][0] for c, _, _ in scomp)
    vmax = max(comps[c][1] for c, _, _ in scomp)
    blocks = []
    for cid, td, ta in scomp:
        h, v = comps[cid]
        blocks += [(huff[(0, td)], huff[(1, ta)])] * (h * v)
    total = -(-width // (8 * hmax)) * -(-height // (8 * vmax))
    out = bytearray()
    done = 0
    for seg, marker in parts:
        n_mcu = min(dri, total - done) if (dri and marker is not None) else total - done
        done += n_mcu
        raw = seg.replace(b"\xff\x00", b"\xff")
        nbits = len(raw) * 8
        buf = raw + b"\x00\x00\x00\x00"
        pos = 0
        acc, accn = 0, 0
        ob = bytearray()
        for _ in range(n_mcu):
            for dct, act in blocks:
                # DC
                p = pos >> 3
                peek = ((buf[p] << 16 | buf[p + 1] << 8 | buf[p + 2]) >> (8 - (pos & 7))) & 0xFFFF
                e = dct[peek]
                if e is None:
                    return None
                ln, s = e
                acc = (acc << ln) | (peek >> (16 - ln)); accn += ln
                pos += ln
                if s:
                    p = pos >> 3
                    val = ((buf[p] << 16 | buf[p + 1] << 8 | buf[p + 2]) >> (24 - s - (pos & 7))) & ((1 << s) - 1)
                    acc = (acc << s) | (val ^ ((1 << s) - 1)); accn += s
                    pos += s
                k = 1
                while k < 64:
                    p = pos >> 3
                    peek = ((buf[p] << 16 | buf[p + 1] << 8 | buf[p + 2]) >> (8 - (pos & 7))) & 0xFFFF
                    e = act[peek]
                    if e is None:
                        return None
                    ln, rs = e
                    acc = (acc << ln) | (peek >> (16 - ln)); accn += ln
                    pos += ln
                    r, s = rs >> 4, rs & 15
                    if s == 0:
                        if r == 15:
                            k += 16
                            continue
                        break  # EOB
                    k += r
                    p = pos >> 3
                    val = ((buf[p] << 16 | buf[p + 1] << 8 | buf[p + 2]) >> (24 - s - (pos & 7))) & ((1 << s) - 1)
                    acc = (acc << s) | (val ^ ((1 << s) - 1)); accn += s
                    pos += s
                    k += 1
                while accn >= 8:
                    accn -= 8
                    ob.append((acc >> accn) & 0xFF)
                acc &= (1 << accn) - 1
            if pos > nbits:
                return None
        if accn:
            ob.append(((acc << (8 - accn)) | ((1 << (8 - accn)) - 1)) & 0xFF)
        out += bytes(ob).replace(b"\xff", b"\xff\x00")
        if marker:
            out += marker
    return bytes(out)


def save_bytes(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "wb") as f:
        f.write(data)
    os.replace(path + ".tmp", path)


def download_image(url, source_id):
    ext = os.path.splitext(url.split("?")[0])[1].lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        ext = ".jpg"
    ext = ".jpg" if ext == ".jpeg" else ext
    rel = "sources/%s/images/%s%s" % (KEY, source_id, ext)
    dest = os.path.join(IMAGES, source_id + ext)
    if not os.path.exists(dest):
        data = fetch(url, binary=True)
        if not (data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n" or data[:4] in (b"GIF8", b"RIFF")):
            raise Blocked("not an image")
        save_bytes(dest, data)
    return rel


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(argv):
    fetch_only = "--fetch-only" in argv
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(IMAGES, exist_ok=True)
    recipes, skipped, notes = [], [], []
    jp2_saved = []

    # ---- inventory
    editions, landing_links = list_editions()
    ed_lists = []
    claimed_total = 0
    for ed in editions:
        claimed, items = list_edition_pdfs(ed)
        ed_lists.append((ed, claimed, items))
        claimed_total += claimed or len(items)
    posts = list_category_posts()
    all_pdfs = []
    for ed, claimed, items in ed_lists:
        all_pdfs += [u for u, _ in items]
    to_get = list(dict.fromkeys(all_pdfs + [COOKBOOK_URL]))

    def get(u):
        try:
            fetch(u, binary=True)
            return u, None
        except Blocked as e:
            return u, str(e)

    failed = {}
    with ThreadPoolExecutor(max_workers=3) as ex:
        for u, err in ex.map(get, to_get):
            if err:
                failed[u] = err
    post_pages = {}
    for u, t in posts:
        try:
            post_pages[u] = fetch(u)
        except Blocked as e:
            failed[u] = str(e)
    if fetch_only:
        print("fetched; failures:", failed)
        return

    # ---- edition PDFs
    listed_pdf_entries = 0
    for ed, claimed, items in ed_lists:
        n = edition_number(ed)
        by_url = {}
        for u, t in items:
            by_url.setdefault(u, []).append(t)
        if claimed is not None and claimed != len(items):
            notes.append("%s edition page says %d recipes but links %d" % (ordinal(n), claimed, len(items)))
        for u, titles in by_url.items():
            listed_pdf_entries += len(titles)
            if u in failed:
                for t in titles:
                    skipped.append({"title": t, "url": u, "edition": n, "reason": "fetch failed: " + failed[u]})
                continue
            data = fetch(u, binary=True)
            try:
                rec = parse_pdf_recipe(data)
            except Exception as e:  # pragma: no cover - defensive
                for t in titles:
                    skipped.append({"title": t, "url": u, "edition": n, "reason": "PDF parse error: %s" % e})
                continue
            pdf_title = smart_title(rec["title_pdf"] or "") if rec["title_pdf"] else None
            chosen = titles[0]
            if pdf_title and len(titles) > 1:
                chosen = max(titles, key=lambda t: difflib.SequenceMatcher(None, t.lower(), pdf_title.lower()).ratio())
            for t in titles:
                if t is not chosen:
                    skipped.append({"title": t, "url": u, "edition": n,
                                    "reason": "edition page links this title to the PDF of another recipe (%s); "
                                              "its own recipe text is not on aakp.org" % (pdf_title or chosen)})
            if not (rec["ingredients"] and rec["steps"]):
                skipped.append({"title": chosen, "url": u, "edition": n,
                                "reason": "PDF has no extractable ingredients/steps"})
                continue
            title = pdf_title if pdf_title and len(re.findall(r"[A-Za-z]", pdf_title)) >= 3 else chosen
            if re.sub(r"\W", "", title).lower() == re.sub(r"\W", "", chosen).lower():
                title = chosen   # same words; the listing has cleaner spacing than the PDF's display type
            title = re.sub(r"(\w)- (\w)", r"\1-\2", title)
            r = empty_record()
            r["source_id"] = "ed%d-%s" % (n, slugify(title))
            r["url"] = u
            r["title"] = title
            r["description"] = rec.get("description")
            times = rec["times"]
            r["prep_time"], r["cook_time"], r["total_time"] = times["prep_time"], times["cook_time"], times["total_time"]
            r["serving_size"] = rec["serving_size"]
            r["portions"] = times["portions"] or portions_from_serving(rec["serving_size"])
            if r["serving_size"] and r["serving_size"].lower().startswith("of recipe") and r["portions"] and \
                    re.fullmatch(r"\d+", r["portions"]):
                r["serving_size"] = "1/%s of recipe" % r["portions"]   # fraction glyph has no text mapping
            r["nutrients"] = rec["nutrients"]
            r["nutrients_raw"] = rec["nutrients_raw"]
            r["food_choices"] = rec["food_choices"]
            r["diet"] = rec["diet"]
            r["ingredients"], r["steps"], r["hints"] = rec["ingredients"], rec["steps"], rec["hints"]
            im = rec.get("image")
            if im and im.get("raw"):
                dest = os.path.join(IMAGES, r["source_id"] + ".jpg")
                if not os.path.exists(dest):
                    raw = im["raw"]
                    if im.get("cs") == "DeviceCMYK" and not im.get("decode"):
                        # PDF stores plain (non-inverted) CMYK/YCCK, but the JPEG carries an Adobe marker, so
                        # viewers would invert it: negate the DCT coefficients losslessly to compensate.
                        fixed = invert_jpeg_coefficients(raw)
                        if fixed:
                            raw = fixed
                        else:
                            notes.append("CMYK photo left as-is for %s" % r["source_id"])
                    save_bytes(dest, raw)
                r["image_path"] = "sources/%s/images/%s.jpg" % (KEY, r["source_id"])
                r["_image_cs"] = im.get("cs")
            r["_edition"] = n
            recipes.append(finish_record(r))

    # ---- Children's National cookbook (linked from the listing page)
    cookbook_count = 0
    if COOKBOOK_URL in failed:
        skipped.append({"title": "Children's National Cookbook", "url": COOKBOOK_URL,
                        "reason": "fetch failed: " + failed[COOKBOOK_URL]})
    else:
        cb, toc = parse_cookbook(fetch(COOKBOOK_URL, binary=True))
        cookbook_count = len(toc)
        if len(cb) != len(toc):
            notes.append("cookbook TOC lists %d recipes, parsed %d" % (len(toc), len(cb)))
        for c in cb:
            r = empty_record()
            r["source_id"] = "childrens-national-" + slugify(c["title"])
            r["url"] = COOKBOOK_URL + "#page=%d" % (c["page"] + 1)
            r["title"] = c["title"]
            r["description"] = c["subtitle"]
            sv = c["serves"]
            m = re.match(r"^Serves\s+(\d+)", sv or "", re.I)
            m2 = re.match(r"^Makes\s+(.+?)(?:,\s*Serving Size is\s+(.+))?$", sv or "", re.I)
            if m:
                r["portions"] = m.group(1)
            elif m2:
                r["portions"] = m2.group(1).lower()
                r["serving_size"] = m2.group(2).lower() if m2.group(2) else None
            r["nutrients"], r["nutrients_raw"] = c["nutrients"], c["nutrients_raw"]
            r["ingredients"], r["steps"], r["hints"] = c["ingredients"], c["steps"], c["hints"]
            region = (c["toc"] or {}).get("region", "")
            cz = []
            for key, vals in CUISINE_MAP:
                if key in region.lower():
                    cz += [v for v in vals if v not in cz]
                    break
            r["cuisine"] = cz
            if c["images"]:
                im = max(c["images"], key=lambda i: (i["w"] or 0) * (i["h"] or 0))
                pdf = None
            r["_cookbook_page"] = c["page"]
            r["_cookbook_images"] = c["images"]
            recipes.append(finish_record(r))
        # embedded cookbook photos are JPEG 2000; extract raw bytes as .jp2
        cbdata = fetch(COOKBOOK_URL, binary=True)
        cbpdf = None
        jp2_saved = []
        for r in recipes:
            ims = r.pop("_cookbook_images", None)
            if not ims:
                continue
            im = max(ims, key=lambda i: (i["w"] or 0) * (i["h"] or 0))
            if cbpdf is None:
                cbpdf = PDF(cbdata)
            d, _ = cbpdf.get(im["ref"])
            raw = d.get("_raw_stream") if isinstance(d, dict) else None
            if raw and raw[:12] in (b"\x00\x00\x00\x0cjP  \r\n\x87\n",) or (raw and raw[:4] == b"\xff\x4f\xff\x51"):
                ext = ".jp2" if raw[:4] != b"\xff\x4f\xff\x51" else ".j2k"
                dest = os.path.join(IMAGES, r["source_id"] + ext)
                if not os.path.exists(dest):
                    save_bytes(dest, raw)
                jp2_saved.append(r["source_id"])   # not browser-viewable, so image_path stays null

    # ---- HTML recipe posts
    for u, t in posts:
        if u in failed:
            skipped.append({"title": t, "url": u, "reason": "fetch failed: " + failed[u]})
            continue
        rec = parse_html_post(u, post_pages[u])
        if not rec["ingredients"] or not rec["steps"]:
            skipped.append({"title": t, "url": u, "reason": "category 'Recipe' post that is not a recipe "
                                                            "(article / roundup without ingredients and steps)"})
            continue
        r = empty_record()
        slug = u.rstrip("/").rsplit("/", 1)[-1]
        r["source_id"] = slug
        r["url"] = u
        r["title"] = rec["title"] or t
        r["serving_size"], r["portions"] = rec["serving_size"], rec["portions"]
        r["nutrients"], r["nutrients_raw"] = rec["nutrients"], rec["nutrients_raw"]
        r["food_choices"], r["carb_choices"] = rec["food_choices"], rec["carb_choices"]
        r["ingredients"], r["steps"], r["hints"] = rec["ingredients"], rec["steps"], rec["hints"]
        if rec["image_url"]:
            r["image_url"] = rec["image_url"]
            try:
                r["image_path"] = download_image(rec["image_url"], slug)
            except Blocked as e:
                notes.append("image failed for %s: %s" % (slug, e))
        recipes.append(finish_record(r))

    # ---- other links on the listing page that are not recipes hosted on aakp.org
    for href, txt in landing_links:
        if href.endswith(".pdf") and "/2026/04/" in href:
            continue  # 9th edition, also listed on its edition page
        if href == COOKBOOK_URL:
            continue
        low = href.lower()
        if re.search(r"youtube\.com", low):
            skipped.append({"title": txt, "url": href, "reason": "video playlist (YouTube), no recipe text on aakp.org"})
        elif re.search(r"davita|dciinc|fresenius|nwkidney|rshope|kidneyfund|eatright", low):
            skipped.append({"title": txt, "url": href, "reason": "external site, not hosted on aakp.org"})
        elif low.endswith(".pdf"):
            skipped.append({"title": txt, "url": href, "reason": "nutrition guide PDF, not a recipe"})
        elif "/product/" in low:
            skipped.append({"title": txt, "url": href, "reason": "store page for printed recipe cards "
                                                               "(same recipes as the digital edition PDFs); not fetched"})

    # ---- de-duplicate source_ids
    seen = {}
    for r in recipes:
        sid = r["source_id"]
        if sid in seen:
            seen[sid] += 1
            r["source_id"] = "%s-%d" % (sid, seen[sid])
            if r["image_path"]:
                old = os.path.join(HERE, "..", "..", r["image_path"])
                ext = os.path.splitext(r["image_path"])[1]
                new_rel = "sources/%s/images/%s%s" % (KEY, r["source_id"], ext)
                try:
                    os.replace(os.path.join(IMAGES, sid + ext), os.path.join(IMAGES, r["source_id"] + ext))
                except OSError:
                    pass
                r["image_path"] = new_rel
        else:
            seen[sid] = 1

    cmyk = sum(1 for r in recipes if r.get("_image_cs") == "DeviceCMYK")
    for r in recipes:
        r.pop("_image_cs", None)
        r.pop("_edition", None)
        r.pop("_cookbook_page", None)

    with open(os.path.join(HERE, "recipes.json"), "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, "skipped.json"), "w", encoding="utf-8") as f:
        json.dump(skipped, f, ensure_ascii=False, indent=1)

    listed = listed_pdf_entries + cookbook_count + len(posts)
    with_img = sum(1 for r in recipes if r["image_path"])
    with_nut = sum(1 for r in recipes if any(v is not None for v in r["nutrients"].values()))
    note = (
        "Sources: 9 'AAKP Delicious!' edition pages (listing claims %d recipes; %d PDF links) + Children's National "
        "cookbook PDF linked from the listing (%d recipes in its TOC) + %d posts in the WordPress 'Recipe' category. "
        "listed = %d edition links + %d cookbook recipes + %d category posts. WP REST API (/wp-json/) is behind a "
        "Cloudflare managed challenge, so HTML listings were used instead. All recipe cards are PDFs on aakp.org, "
        "parsed with a built-in stdlib PDF text extractor (no pdftotext available). Same-titled recipes in different "
        "editions are separate PDFs with their own analyses and are kept as separate records (source_id prefixed "
        "edN-). Photos: recipe-card photos are the JPEGs embedded in each PDF (image_url null, image_path set; %d "
        "of them are CMYK JPEGs whose DCT coefficients were negated losslessly so that viewers applying the Adobe CMYK "
        "convention show correct colours); the %d Children's National cookbook photos are embedded JPEG 2000: they "
        "are saved as images/<source_id>.jp2 for reference but image_path is left null because browsers cannot show "
        "them; HTML posts use the WordPress featured image. Diet comes from the ticked 'Diet Types' boxes "
        "(Transplant has no matching diet value and is omitted). %s"
        % (claimed_total, listed_pdf_entries, cookbook_count, len(posts), listed_pdf_entries, cookbook_count,
           len(posts), cmyk, len(jp2_saved), " ".join(notes))
    )
    report = {"listed": listed, "scraped": len(recipes), "with_image": with_img, "with_nutrients": with_nut,
              "skipped": len(skipped), "notes": note.strip()}
    with open(os.path.join(HERE, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(json.dumps(report, indent=1))


def ordinal(n):
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n if n < 20 else n % 10, "th"))


if __name__ == "__main__":
    main(sys.argv[1:])
