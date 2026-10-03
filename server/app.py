#!/usr/bin/env python3
"""Health Kitchen API: accounts, per-user state and admin, on a local PostgreSQL.

Serves the gallery (../gallery) at / and the API under /api. Every request that touches
user data runs in a transaction with hk.user_id / hk.role set, so PostgreSQL row-level
security limits it to that user's rows (admins see all).

Run:  server/run.sh   (serves the app, accounts and admin on http://localhost:8099)
Env:  HK_DB_URL (default postgresql://hk_api:hk_api_dev_pw@127.0.0.1:5440/health_kitchen)
"""
import hashlib
import json
import os
import re
import secrets
from contextlib import contextmanager
from datetime import date
from pathlib import Path

import psycopg
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic import BaseModel, Field

HERE = Path(__file__).resolve().parent
GALLERY = HERE.parent / "gallery"
CONFIG_FILE = HERE / "config.json"   # written by the Admin page (database connection); not in git
_file_cfg = json.loads(CONFIG_FILE.read_text()) if CONFIG_FILE.exists() else {}
DB_URL = _file_cfg.get("db_url") or os.environ.get("HK_DB_URL", "postgresql://hk_api:hk_api_dev_pw@127.0.0.1:5440/health_kitchen")
SESSION_DAYS = 30
pool = ConnectionPool(DB_URL, min_size=1, max_size=8, open=True)
DEFAULT_CONFIG = {"defaults": {"lang": "", "theme": "", "units": "", "plan": ""}, "allow_signups": True, "session_days": 30,
                  "announcement": {"active": False, "level": "info", "text": {}}, "hidden_sources": [], "hidden_langs": []}
app = FastAPI(title="Health Kitchen API")
# the app may also be opened from another local port (e.g. a plain file server); allow those pages to call the API
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
app.add_middleware(CORSMiddleware, allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
                   allow_methods=["*"], allow_headers=["*"])


# ---------- passwords and tokens ----------
def hash_password(pw: str) -> str:
    salt = secrets.token_bytes(16)
    h = hashlib.scrypt(pw.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    return f"scrypt${salt.hex()}${h.hex()}"


def check_password(pw: str, stored: str) -> bool:
    try:
        _, salt, h = stored.split("$")
        got = hashlib.scrypt(pw.encode(), salt=bytes.fromhex(salt), n=2 ** 14, r=8, p=1, dklen=32)
        return secrets.compare_digest(got.hex(), h)
    except Exception:  # noqa: BLE001
        return False


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


@contextmanager
def as_user(uid=None, role="user"):
    """A transaction in which RLS sees the given user."""
    with pool.connection() as conn:
        conn.row_factory = dict_row
        with conn.transaction():
            conn.execute("SELECT set_config('hk.user_id', %s, true), set_config('hk.role', %s, true)",
                         (str(uid) if uid else "", role))
            yield conn


def current(authorization: str = Header(default="")):
    tok = authorization.removeprefix("Bearer ").strip()
    if not tok:
        raise HTTPException(401, "Sign in required")
    with as_user() as c:
        row = c.execute("SELECT * FROM hk.session_user_of(%s)", (token_hash(tok),)).fetchone()
    if not row:
        raise HTTPException(401, "Session expired, please sign in again")
    return {"id": row["id"], "role": row["role"], "token": tok}


def admin(user=Depends(current)):
    if user["role"] != "admin":
        raise HTTPException(403, "Admins only")
    return user


# ---------- auth ----------
class SignUp(BaseModel):
    email: str = Field(max_length=200)
    password: str = Field(min_length=8, max_length=200)
    name: str = Field(default="", max_length=100)


class Login(BaseModel):
    email: str
    password: str


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def app_config(c) -> dict:
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    for row in c.execute("SELECT key, value FROM hk.app_config").fetchall():
        cfg[row["key"]] = row["value"]
    return cfg


def new_session(c, uid):
    tok = secrets.token_urlsafe(32)
    days = int(app_config(c).get("session_days") or SESSION_DAYS)
    c.execute("SELECT hk.start_session(%s, %s, %s)", (uid, token_hash(tok), max(1, min(days, 365))))
    return tok


@app.post("/api/signup")
def signup(body: SignUp):
    if not EMAIL_RE.match(body.email):
        raise HTTPException(400, "Enter a valid email address")
    with as_user() as c:
        if not app_config(c).get("allow_signups", True):
            raise HTTPException(403, "New sign-ups are closed")
        try:
            row = c.execute("SELECT * FROM hk.create_user(%s, %s, %s)",
                            (body.email.strip(), hash_password(body.password), body.name.strip())).fetchone()
        except psycopg.errors.UniqueViolation:
            raise HTTPException(409, "An account with this email already exists")
        tok = new_session(c, row["id"])
    with as_user(row["id"], row["role"]) as c:
        c.execute("INSERT INTO hk.user_state (user_id) VALUES (%s) ON CONFLICT DO NOTHING", (row["id"],))
    return {"token": tok, "role": row["role"]}


@app.post("/api/login")
def login(body: Login):
    with as_user() as c:
        row = c.execute("SELECT * FROM hk.login_lookup(%s)", (body.email.strip(),)).fetchone()
        if not row or not check_password(body.password, row["password_hash"]):
            raise HTTPException(401, "Email or password is incorrect")
        if row["disabled"]:
            raise HTTPException(403, "This account is disabled")
        tok = new_session(c, row["id"])
    return {"token": tok, "role": row["role"]}


@app.post("/api/logout")
def logout(user=Depends(current)):
    with as_user(user["id"], user["role"]) as c:
        c.execute("SELECT hk.end_session(%s)", (token_hash(user["token"]),))
    return {"ok": True}


# ---------- the signed-in user's data ----------
class State(BaseModel):
    profile: dict = {}
    plan: dict = {}
    settings: dict = {}
    favs: list = []
    day: list = []
    day_date: date | None = None
    history: dict = {}
    weights: list = []          # [{d: "YYYY-MM-DD", kg}]
    name: str | None = None


@app.get("/api/me")
def me(user=Depends(current)):
    with as_user(user["id"], user["role"]) as c:
        u = c.execute("SELECT id, email, name, role, created_at FROM hk.users WHERE id = %s", (user["id"],)).fetchone()
        st = c.execute("SELECT profile, plan, settings, favs, day, day_date, history, updated_at FROM hk.user_state WHERE user_id = %s",
                       (user["id"],)).fetchone() or {}
        w = c.execute("SELECT d, kg FROM hk.weights WHERE user_id = %s ORDER BY d", (user["id"],)).fetchall()
    return {"user": u, "state": st, "weights": [{"d": x["d"].isoformat(), "kg": float(x["kg"])} for x in w]}


@app.put("/api/me")
def save_me(body: State, user=Depends(current)):
    uid = user["id"]
    with as_user(uid, user["role"]) as c:
        c.execute("""INSERT INTO hk.user_state (user_id, profile, plan, settings, favs, day, day_date, history, updated_at)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())
                     ON CONFLICT (user_id) DO UPDATE SET profile = EXCLUDED.profile, plan = EXCLUDED.plan, settings = EXCLUDED.settings,
                       favs = EXCLUDED.favs, day = EXCLUDED.day, day_date = EXCLUDED.day_date, history = EXCLUDED.history, updated_at = now()""",
                  (uid, json.dumps(body.profile), json.dumps(body.plan), json.dumps(body.settings), json.dumps(body.favs),
                   json.dumps(body.day), body.day_date, json.dumps(body.history)))
        c.execute("DELETE FROM hk.weights WHERE user_id = %s", (uid,))
        for w in body.weights[-2000:]:
            try:
                c.execute("INSERT INTO hk.weights (user_id, d, kg) VALUES (%s, %s, %s) ON CONFLICT (user_id, d) DO UPDATE SET kg = EXCLUDED.kg",
                          (uid, w["d"], float(w["kg"])))
            except (KeyError, ValueError, TypeError):
                continue
        if body.name is not None:
            c.execute("UPDATE hk.users SET name = %s WHERE id = %s", (body.name[:100], uid))
    return {"ok": True}


# ---------- admin ----------
@app.get("/api/admin/stats")
def admin_stats(user=Depends(admin)):
    with as_user(user["id"], "admin") as c:
        signups = c.execute("""SELECT to_char(d, 'YYYY-MM-DD') AS d, count(u.id) AS n
                               FROM generate_series(current_date - 29, current_date, interval '1 day') d
                               LEFT JOIN hk.users u ON u.created_at::date = d::date GROUP BY d ORDER BY d""").fetchall()
        row = c.execute("""SELECT count(*) AS users,
                                  count(*) FILTER (WHERE role = 'admin') AS admins,
                                  count(*) FILTER (WHERE disabled) AS disabled,
                                  count(*) FILTER (WHERE greatest(last_seen, last_login) > now() - interval '1 day') AS active_day,
                                  count(*) FILTER (WHERE greatest(last_seen, last_login) > now() - interval '7 days') AS active_week,
                                  (SELECT count(*) FROM hk.weights) AS weigh_ins
                           FROM hk.users""").fetchone()
    return {**row, "signups": [{"d": x["d"], "n": x["n"]} for x in signups]}


@app.get("/api/admin/users/{uid}")
def admin_user(uid: str, user=Depends(admin)):
    with as_user(user["id"], "admin") as c:
        u = c.execute("SELECT id, email, name, role, disabled, created_at, last_login, last_seen FROM hk.users WHERE id = %s", (uid,)).fetchone()
        if not u:
            raise HTTPException(404, "Not found")
        st = c.execute("SELECT profile, plan, favs, day, history, updated_at FROM hk.user_state WHERE user_id = %s", (uid,)).fetchone() or {}
        w = c.execute("SELECT d, kg FROM hk.weights WHERE user_id = %s ORDER BY d", (uid,)).fetchall()
    prof = st.get("profile") or {}
    # medical notes stay private to the user; admins see the account and plan summary only
    safe = {k: prof.get(k) for k in ("name", "goal", "target")}
    return {"user": u, "profile": safe, "plan": st.get("plan") or {}, "saved": len(st.get("favs") or []),
            "days_logged": len([k for k in (st.get("history") or {}) if re.match(r"^\d{4}-\d{2}-\d{2}$", k)]),
            "updated_at": st.get("updated_at"), "weights": [{"d": x["d"].isoformat(), "kg": float(x["kg"])} for x in w]}


class NewPassword(BaseModel):
    password: str = Field(min_length=8, max_length=200)


@app.put("/api/admin/users/{uid}/password")
def admin_password(uid: str, body: NewPassword, user=Depends(admin)):
    with as_user(user["id"], "admin") as c:
        c.execute("UPDATE hk.users SET password_hash = %s WHERE id = %s", (hash_password(body.password), uid))
        if uid != str(user["id"]):
            c.execute("SELECT hk.end_user_sessions(%s)", (uid,))
    return {"ok": True}


class Active(BaseModel):
    disabled: bool


@app.put("/api/admin/users/{uid}/disabled")
def admin_disable(uid: str, body: Active, user=Depends(admin)):
    if uid == str(user["id"]):
        raise HTTPException(400, "You can't disable your own account")
    with as_user(user["id"], "admin") as c:
        c.execute("UPDATE hk.users SET disabled = %s WHERE id = %s", (body.disabled, uid))
        if body.disabled:
            c.execute("SELECT hk.end_user_sessions(%s)", (uid,))
    return {"ok": True}


@app.get("/api/admin/users")
def admin_users(user=Depends(admin)):
    with as_user(user["id"], "admin") as c:
        rows = c.execute("""SELECT u.id, u.email, u.name, u.role, u.disabled, u.created_at, u.last_login, u.last_seen,
                                   s.plan->>'type' AS plan_type, jsonb_array_length(coalesce(s.favs, '[]')) AS saved,
                                   (SELECT count(*) FROM hk.weights w WHERE w.user_id = u.id) AS weigh_ins,
                                   (SELECT kg FROM hk.weights w WHERE w.user_id = u.id ORDER BY d DESC LIMIT 1) AS last_kg,
                                   s.updated_at
                            FROM hk.users u LEFT JOIN hk.user_state s ON s.user_id = u.id ORDER BY u.created_at""").fetchall()
    return {"users": [{**r, "last_kg": float(r["last_kg"]) if r["last_kg"] is not None else None} for r in rows]}


@app.delete("/api/admin/users/{uid}")
def admin_delete(uid: str, user=Depends(admin)):
    if uid == str(user["id"]):
        raise HTTPException(400, "You can't delete your own account here")
    with as_user(user["id"], "admin") as c:
        c.execute("DELETE FROM hk.users WHERE id = %s", (uid,))
    return {"ok": True}


# ---------- app settings and database (Admin page) ----------
@app.get("/api/config")
def public_config():
    with as_user() as c:
        cfg = app_config(c)
    return {k: cfg[k] for k in ("defaults", "allow_signups", "announcement", "hidden_sources", "hidden_langs")}


@app.get("/api/admin/config")
def get_config(user=Depends(admin)):
    with as_user(user["id"], "admin") as c:
        return app_config(c)


@app.put("/api/admin/config")
def put_config(body: dict, user=Depends(admin)):
    allowed = set(DEFAULT_CONFIG)
    with as_user(user["id"], "admin") as c:
        for k, v in body.items():
            if k not in allowed:
                raise HTTPException(400, f"Unknown setting: {k}")
            if k == "session_days" and not (isinstance(v, int) and 1 <= v <= 365):
                raise HTTPException(400, "Session length must be 1 to 365 days")
            c.execute("""INSERT INTO hk.app_config (key, value, updated_at) VALUES (%s, %s, now())
                         ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now()""", (k, json.dumps(v)))
    return {"ok": True}


def mask_url(url: str) -> str:
    return re.sub(r"//([^:/@]+):[^@]*@", r"//\1:•••@", url)


def db_info(conn) -> dict:
    conn.row_factory = dict_row
    r = conn.execute("""SELECT current_database() AS database, current_user AS "user", inet_server_addr()::text AS host,
                        inet_server_port() AS port, version() AS version, pg_size_pretty(pg_database_size(current_database())) AS size""").fetchone()
    r["schema_ready"] = conn.execute("SELECT to_regclass('hk.users') IS NOT NULL AS ok").fetchone()["ok"]
    return r


@app.get("/api/admin/database")
def database_status(user=Depends(admin)):
    with as_user(user["id"], "admin") as c:
        info = db_info(c)
        counts = {t: c.execute(f"SELECT count(*) AS n FROM hk.{t}").fetchone()["n"] for t in ("users", "user_state", "weights", "submissions")}
    return {**info, "url": mask_url(DB_URL), "counts": counts, "pool": {"min": pool.min_size, "max": pool.max_size},
            "supported": ["PostgreSQL 13+ (local, Docker, Supabase, Neon, AWS RDS, Azure, Google Cloud SQL)"]}


class DbUrl(BaseModel):
    url: str = Field(min_length=12, max_length=500)


def check_url(url: str):
    if not re.match(r"^postgres(ql)?://", url):
        raise HTTPException(400, "Only PostgreSQL connection URLs are supported (postgresql://user:password@host:port/database)")


@app.post("/api/admin/database/test")
def database_test(body: DbUrl, user=Depends(admin)):
    check_url(body.url)
    try:
        with psycopg.connect(body.url, connect_timeout=8) as conn:
            info = db_info(conn)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(400, f"Could not connect: {str(e).splitlines()[0][:200]}")
    return info


@app.post("/api/admin/database/setup")
def database_setup(body: DbUrl, user=Depends(admin)):
    """Create the Health Kitchen tables, security rules and functions on a database (needs an owner/admin URL)."""
    check_url(body.url)
    try:
        with psycopg.connect(body.url, connect_timeout=8, autocommit=True) as conn:
            conn.execute((HERE / "schema.sql").read_text())
            info = db_info(conn)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(400, f"Setup failed: {str(e).splitlines()[0][:200]}")
    return info


@app.put("/api/admin/database")
def database_switch(body: DbUrl, user=Depends(admin)):
    """Point the server at another database (the API user's URL). The current admin must exist there to keep access."""
    global pool, DB_URL
    check_url(body.url)
    try:
        with psycopg.connect(body.url, connect_timeout=8) as conn:
            info = db_info(conn)
            if not info["schema_ready"]:
                raise HTTPException(400, "Tables are missing on that database. Run 'Set up tables' first.")
    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        raise HTTPException(400, f"Could not connect: {str(e).splitlines()[0][:200]}")
    old = pool
    pool = ConnectionPool(body.url, min_size=1, max_size=8, open=True)
    DB_URL = body.url
    cfg = json.loads(CONFIG_FILE.read_text()) if CONFIG_FILE.exists() else {}
    cfg["db_url"] = body.url
    CONFIG_FILE.write_text(json.dumps(cfg, indent=1))
    os.chmod(CONFIG_FILE, 0o600)
    old.close()
    return {"ok": True, "url": mask_url(body.url)}


# ---------- community recipes (published after an admin approves them) ----------
CATEGORIES = {"Appetizers & Snacks", "Beef, Lamb & Pork", "Beverages", "Breads", "Breakfast & Brunch", "Chicken & Turkey", "Desserts",
              "Fish & Seafood", "Pasta, Rice & Grains", "Pizza & Sandwiches", "Salads & Dressings", "Sauces & Seasonings", "Soups & Stews", "Vegetables"}
UNITS = {"g", "kg", "ml", "l", "tsp", "tbsp", "piece", "pinch", "clove", "slice", "to taste"}
NUTRIENTS = ("calories", "protein_g", "carbohydrates_g", "fat_g", "cholesterol_mg", "sodium_mg", "potassium_mg", "phosphorus_mg",
             "calcium_mg", "fiber_g", "added_sugar_g")


class Ingredient(BaseModel):
    qty: float | None = Field(default=None, ge=0, le=100000)
    unit: str
    item: str = Field(min_length=1, max_length=200)
    group: str | None = Field(default=None, max_length=80)


class RecipeIn(BaseModel):
    lang: str = Field(pattern=r"^(en|es|ar|ur|hi|fr|id|bn|tl)$")
    title: str = Field(min_length=3, max_length=140)
    description: str = Field(default="", max_length=1000)
    category: str
    cuisine: str = Field(default="", max_length=60)
    servings: int = Field(ge=1, le=60)
    serving_size: str = Field(default="", max_length=80)
    ingredients: list[Ingredient] = Field(min_length=1, max_length=60)
    steps: list[str] = Field(min_length=1, max_length=40)
    hints: list[str] = Field(default=[], max_length=20)
    nutrients: dict[str, float | None] = {}


_L = r"A-Za-z\u00C0-\u024F\u0600-\u06FF\u0900-\u097F\u0980-\u09FF"
EXCLUDED = re.compile("|".join(rf"(?<![{_L}]){w}(?![{_L}])" for w in (
    "pork", "bacon", "ham", "lard", "prosciutto", "pancetta", "pepperoni", "salami", "gelatine?", "jell-?o", "wines?", "beers?", "rum", "brandy",
    "vodka", "whiske?y", "sake", "mirin", "liqueurs?", "sherry", "champagne", "cerdo", "tocino", "jam[oó]n", "vino", "cerveza", "gelatina",
    "porc", "jambon", "vin", "bi[eè]re", "babi", "baboy", "خنزير", "الخنزير", "نبيذ", "النبيذ", "بيرة", "خمر", "كحول", "جيلاتين", "سور", "سूअर",
    "सूअर", "शराब", "वाइन", "बीयर", "শূকর", "মদ", "ওয়াইন"))
    + r"|turkey bacon|beef bacon|wine vinegar|vinagre de vino|خل النبيذ", re.I)
SAFE = re.compile(r"turkey bacon|beef bacon|turkey ham|vinegar|vinagre|vinaigre|خل|سرکہ|सिरका|root beer|ginger beer|non-?alcoholic", re.I)


def has_excluded(rec: dict) -> bool:
    texts = [rec["title"], rec.get("description", "")] + [i["item"] for i in rec["ingredients"]] + rec["steps"] + rec.get("hints", [])
    for t in texts:
        for m in EXCLUDED.finditer(t or ""):
            if not SAFE.search(t[max(0, m.start() - 12): m.end() + 12]):
                return True
    return False


def clean_recipe(body: RecipeIn) -> dict:
    if body.category not in CATEGORIES:
        raise HTTPException(400, "Unknown category")
    for i in body.ingredients:
        if i.unit not in UNITS:
            raise HTTPException(400, f"Unit not allowed: {i.unit}")
        if i.unit not in ("to taste", "pinch") and not i.qty:
            raise HTTPException(400, f"Amount missing for: {i.item}")
    steps = [x.strip() for x in body.steps if x.strip()]
    if not steps:
        raise HTTPException(400, "Add at least one step")
    nut = {k: (float(v) if v is not None and v >= 0 else None) for k, v in body.nutrients.items() if k in NUTRIENTS}
    d = body.model_dump()
    d.update(steps=[x[:1500] for x in steps], hints=[x.strip()[:600] for x in body.hints if x.strip()], nutrients=nut)
    if has_excluded(d):
        raise HTTPException(400, "This recipe contains an ingredient the app does not include (pork, gelatin or alcohol)")
    return d


@app.post("/api/submissions")
def submit_recipe(body: RecipeIn, user=Depends(current)):
    rec = clean_recipe(body)
    with as_user(user["id"], user["role"]) as c:
        n = c.execute("SELECT count(*) AS n FROM hk.submissions WHERE user_id = %s AND status = 'pending'", (user["id"],)).fetchone()["n"]
        if n >= 20:
            raise HTTPException(429, "Too many recipes waiting for review")
        row = c.execute("INSERT INTO hk.submissions (user_id, recipe) VALUES (%s, %s) RETURNING id", (user["id"], json.dumps(rec))).fetchone()
    return {"id": row["id"], "status": "pending"}


@app.get("/api/submissions/mine")
def my_submissions(user=Depends(current)):
    with as_user(user["id"], user["role"]) as c:
        rows = c.execute("SELECT id, recipe, status, admin_note, created_at, reviewed_at FROM hk.submissions WHERE user_id = %s ORDER BY created_at DESC",
                         (user["id"],)).fetchall()
    return {"items": rows}


@app.delete("/api/submissions/{sid}")
def delete_submission(sid: int, user=Depends(current)):
    with as_user(user["id"], user["role"]) as c:
        c.execute("DELETE FROM hk.submissions WHERE id = %s AND user_id = %s AND status <> 'approved'", (sid, user["id"]))
    return {"ok": True}


@app.get("/api/recipes/community")
def community_recipes():
    with as_user() as c:
        rows = c.execute("SELECT * FROM hk.approved_recipes()").fetchall()
    return {"items": rows}


@app.get("/api/admin/submissions")
def admin_submissions(status: str = "pending", user=Depends(admin)):
    with as_user(user["id"], "admin") as c:
        rows = c.execute("""SELECT s.id, s.recipe, s.status, s.admin_note, s.created_at, s.reviewed_at, u.email, u.name
                            FROM hk.submissions s JOIN hk.users u ON u.id = s.user_id
                            WHERE %s = 'all' OR s.status = %s ORDER BY s.created_at""", (status, status)).fetchall()
    return {"items": rows}


class Review(BaseModel):
    status: str = Field(pattern=r"^(approved|rejected|pending)$")
    admin_note: str = Field(default="", max_length=1000)
    recipe: RecipeIn | None = None


@app.put("/api/admin/submissions/{sid}")
def review_submission(sid: int, body: Review, user=Depends(admin)):
    with as_user(user["id"], "admin") as c:
        if body.recipe is not None:
            c.execute("UPDATE hk.submissions SET recipe = %s WHERE id = %s", (json.dumps(clean_recipe(body.recipe)), sid))
        c.execute("UPDATE hk.submissions SET status = %s, admin_note = %s, reviewed_at = now() WHERE id = %s", (body.status, body.admin_note, sid))
    return {"ok": True}


@app.get("/api/health")
def health():
    with as_user() as c:
        c.execute("SELECT 1")
    return {"ok": True}


# ---------- the app itself ----------
@app.get("/")
def index():
    return FileResponse(GALLERY / "index.html")


@app.get("/gallery")
@app.get("/gallery/")
def old_gallery_path():
    # links from the old static server (http://localhost:8099/gallery/#...) keep working; the #hash stays in the browser
    from fastapi.responses import RedirectResponse
    return RedirectResponse("/", status_code=307)


app.mount("/", StaticFiles(directory=GALLERY), name="gallery")
