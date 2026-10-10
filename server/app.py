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
import time
from contextlib import contextmanager
from datetime import date
from pathlib import Path

import psycopg
import psycopg.sql
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic import BaseModel, Field

HERE = Path(__file__).resolve().parent
GALLERY = HERE.parent / "gallery"
CONFIG_FILE = HERE / "config.json"   # written by the Admin page (database connection, encrypted); not in git
KEY_FILE = HERE / ".hk_secret"        # encryption key for config.json; not in git
from cryptography.fernet import Fernet  # noqa: E402


def _fernet() -> Fernet:
    if not KEY_FILE.exists():
        KEY_FILE.write_bytes(Fernet.generate_key())
        os.chmod(KEY_FILE, 0o600)
    return Fernet(KEY_FILE.read_bytes())


def read_cfg() -> dict:
    cfg = json.loads(CONFIG_FILE.read_text()) if CONFIG_FILE.exists() else {}
    if "db_url" in cfg:   # older plain-text setting: encrypt it now
        cfg["db_url_enc"] = _fernet().encrypt(cfg.pop("db_url").encode()).decode()
        write_cfg(cfg)
    return cfg


def write_cfg(cfg: dict):
    CONFIG_FILE.write_text(json.dumps(cfg, indent=1))
    os.chmod(CONFIG_FILE, 0o600)


_enc = read_cfg().get("db_url_enc")
DB_URL = (_fernet().decrypt(_enc.encode()).decode() if _enc else None) or os.environ.get(
    "HK_DB_URL", "postgresql://hk_api:hk_api_dev_pw@127.0.0.1:5440/health_kitchen")
SESSION_DAYS = 30
pool = ConnectionPool(DB_URL, min_size=1, max_size=8, open=True)
DEFAULT_CONFIG = {"defaults": {"lang": "", "theme": "", "units": "", "plan": ""}, "allow_signups": True, "session_days": 30,
                  "announcement": {"active": False, "level": "info", "text": {}}, "hidden_sources": [], "hidden_langs": [], "access": {}, "idle_minutes": 60}
app = FastAPI(title="Health Kitchen API")
# the app may also be opened from another local port (e.g. a plain file server); allow those pages to call the API
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.middleware.gzip import GZipMiddleware  # noqa: E402
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ---------- security: headers on every response, request size limit ----------
SEC_HEADERS = {"X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Referrer-Policy": "strict-origin-when-cross-origin",
               "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
               "Cross-Origin-Opener-Policy": "same-origin", "Cross-Origin-Resource-Policy": "same-site"}
MAX_BODY = 2_000_000


@app.middleware("http")
async def security_headers(request, call_next):
    size = request.headers.get("content-length", "")
    if size.isdigit() and int(size) > MAX_BODY:
        return JSONResponse({"detail": "Request too large"}, status_code=413)
    resp = await call_next(request)
    for k, v in SEC_HEADERS.items():
        resp.headers.setdefault(k, v)
    return resp


@app.middleware("http")
async def cache_headers(request, call_next):
    resp = await call_next(request)
    p, q = request.url.path, request.url.query
    if p.startswith("/api/"):
        resp.headers["Cache-Control"] = "no-store"
    elif q.startswith("v=") or p.startswith(("/fonts/", "/thumbs/", "/photos/")) or p.endswith((".png", ".svg", ".webp")):
        resp.headers["Cache-Control"] = "public, max-age=31536000, immutable" if q.startswith("v=") else "public, max-age=604800"
    elif p in ("/", "/index.html"):
        resp.headers["Cache-Control"] = "no-cache"
    return resp


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


# ---------- sign-in protection: failed attempts per email and per address, password rule, audit log ----------
FAILS: dict[str, list[float]] = {}
LOCK_WINDOW, MAX_PER_EMAIL, MAX_PER_IP = 900, 5, 30


def client_ip(request: Request) -> str:
    return request.client.host if request.client else ""


def throttle_check(*keys_limits):
    now = time.time()
    for key, limit in keys_limits:
        recent = [t for t in FAILS.get(key, []) if now - t < LOCK_WINDOW]
        FAILS[key] = recent
        if len(recent) >= limit:
            mins = int((LOCK_WINDOW - (now - recent[0])) / 60) + 1
            raise HTTPException(429, f"Too many failed attempts. Try again in {mins} minutes.")


def throttle_fail(*keys):
    for key in keys:
        FAILS.setdefault(key, []).append(time.time())


COMMON_PW = re.compile(r"^(password|passw0rd|qwerty|letmein|welcome|admin|iloveyou|abc123|monkey|dragon|football|baseball|sunshine|"
                       r"princess|master|123123|111111|000000|1q2w3e|qazwsx|zaq12wsx)", re.I)


def check_new_password(pw: str, email: str = ""):
    """At least 10 characters with letters and numbers; not a common password or the email name."""
    name = email.split("@")[0].lower()
    if (len(pw) < 10 or not re.search(r"[A-Za-z\u0600-\u06FF]", pw) or not re.search(r"\d", pw) or COMMON_PW.match(pw)
            or re.fullmatch(r"\d+|(.)\1+", pw) or (len(name) > 3 and name in pw.lower())):
        raise HTTPException(400, "Use at least 10 characters with letters and numbers, and avoid common passwords.")


def audit(c, actor, action: str, target: str = "", detail: dict | None = None, ip: str = ""):
    c.execute("INSERT INTO hk.audit_log (actor, action, target, detail, ip) VALUES (%s, %s, %s, %s, %s)",
              (actor, action, str(target), json.dumps(detail or {}), ip))


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
def signup(body: SignUp, request: Request):
    if not EMAIL_RE.match(body.email):
        raise HTTPException(400, "Enter a valid email address")
    throttle_check(("ip:" + client_ip(request), MAX_PER_IP))
    check_new_password(body.password, body.email)
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
def login(body: Login, request: Request):
    ip, em = client_ip(request), body.email.strip().lower()
    throttle_check(("email:" + em, MAX_PER_EMAIL), ("ip:" + ip, MAX_PER_IP))
    with as_user() as c:
        row = c.execute("SELECT * FROM hk.login_lookup(%s)", (body.email.strip(),)).fetchone()
        failed = not row or not check_password(body.password, row["password_hash"])
    if failed:
        throttle_fail("email:" + em, "ip:" + ip)
        if len(FAILS.get("email:" + em, [])) == MAX_PER_EMAIL:
            with as_user() as c:   # its own transaction, so the entry is kept although the request fails
                audit(c, row["id"] if row else None, "login_locked", em, {"attempts": MAX_PER_EMAIL}, ip)
        raise HTTPException(401, "Email or password is incorrect")
    with as_user() as c:
        FAILS.pop("email:" + em, None)
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
def admin_password(uid: str, body: NewPassword, request: Request, user=Depends(admin)):
    check_new_password(body.password)
    with as_user(user["id"], "admin") as c:
        audit(c, user["id"], "password_reset", uid, ip=client_ip(request))
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
        audit(c, user["id"], "user_disabled" if body.disabled else "user_enabled", uid)
        if body.disabled:
            c.execute("SELECT hk.end_user_sessions(%s)", (uid,))
    return {"ok": True}


class RoleBody(BaseModel):
    role: str = Field(pattern="^(user|supervisor|admin)$")


@app.put("/api/admin/users/{uid}/role")
def admin_role(uid: str, body: RoleBody, user=Depends(admin)):
    """Any role for another user; emails in the admin list always stay admin."""
    if uid == str(user["id"]):
        raise HTTPException(400, "You can't change your own role")
    with as_user(user["id"], "admin") as c:
        row = c.execute("UPDATE hk.users SET role = %s WHERE id = %s RETURNING role", (body.role, uid)).fetchone()
        audit(c, user["id"], "role_changed", uid, {"role": body.role})
    if not row:
        raise HTTPException(404, "No such user")
    return {"ok": True, "role": row["role"]}


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
        email = (c.execute("SELECT email FROM hk.users WHERE id = %s", (uid,)).fetchone() or {}).get("email", "")
        c.execute("DELETE FROM hk.users WHERE id = %s", (uid,))
        audit(c, user["id"], "user_deleted", uid, {"email": email})
    return {"ok": True}


# ---------- app settings and database (Admin page) ----------
@app.get("/api/config")
def public_config():
    with as_user() as c:
        cfg = app_config(c)
    return {k: cfg[k] for k in ("defaults", "allow_signups", "announcement", "hidden_sources", "hidden_langs", "access", "idle_minutes")}


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
            if k == "idle_minutes" and not (isinstance(v, int) and 0 <= v <= 1440):
                raise HTTPException(400, "Idle sign-out must be 0 to 1440 minutes")
            if k == "session_days" and not (isinstance(v, int) and 1 <= v <= 365):
                raise HTTPException(400, "Session length must be 1 to 365 days")
            c.execute("""INSERT INTO hk.app_config (key, value, updated_at) VALUES (%s, %s, now())
                         ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now()""", (k, json.dumps(v)))
        audit(c, user["id"], "settings_changed", ",".join(sorted(body)))
    return {"ok": True}


@app.get("/api/admin/audit")
def admin_audit(user=Depends(admin)):
    with as_user(user["id"], "admin") as c:
        rows = c.execute("""SELECT a.at, a.action, a.target, a.detail, a.ip, coalesce(u.email, '') AS actor_email,
                                   coalesce(t.email, a.target) AS target_label
                            FROM hk.audit_log a LEFT JOIN hk.users u ON u.id = a.actor
                            LEFT JOIN hk.users t ON t.id::text = a.target ORDER BY a.id DESC LIMIT 200""").fetchall()
    return {"items": rows}


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
    return {**info, "url": mask_url(DB_URL), "counts": counts, "encrypted": bool(read_cfg().get("db_url_enc")), "pool": {"min": pool.min_size, "max": pool.max_size},
            "supported": ["PostgreSQL 13+ (local, Docker, Supabase, Neon, AWS RDS, Azure, Google Cloud SQL)"]}


class DbUrl(BaseModel):
    url: str = Field(min_length=12, max_length=500)


def check_url(url: str):
    if not re.match(r"^postgres(ql)?://", url):
        raise HTTPException(400, "Only PostgreSQL connection URLs are supported (postgresql://user:password@host:port/database)")


def explain_db_error(e):
    """A short, actionable message for common connection failures."""
    msg = str(e)
    if "password authentication failed" in msg:
        return ("The database rejected the user name or password. In Supabase open Project Settings → Database, "
                "reset the database password, then enter the new one here (user: postgres).")
    if "Network is unreachable" in msg or "could not translate host name" in msg or "timeout expired" in msg:
        return ("This computer cannot reach that host. If it is a Supabase direct connection (IPv6 only), use the "
                "Session pooler from Supabase → Connect instead: host aws-…pooler.supabase.com, port 5432, user postgres.<project-ref>.")
    return msg.splitlines()[0][:220]


@app.post("/api/admin/database/test")
def database_test(body: dict, user=Depends(admin)):
    """Test a connection without changing anything: a full URL or host/port/database/user/password."""
    url = conn_url(Connect(**{k: v for k, v in body.items() if k in Connect.model_fields}))
    try:
        with psycopg.connect(url, connect_timeout=10) as conn:
            info = db_info(conn)
            info["hk_ready"] = conn.execute("SELECT to_regclass('hk.users') IS NOT NULL AS ok").fetchone()["ok"]
            info["can_create_roles"] = conn.execute("SELECT rolcreaterole OR rolsuper AS ok FROM pg_roles WHERE rolname = current_user").fetchone()["ok"]
    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        raise HTTPException(400, f"Could not connect: {explain_db_error(e)}")
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
        raise HTTPException(400, f"Setup failed: {explain_db_error(e)}")
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
        raise HTTPException(400, f"Could not connect: {explain_db_error(e)}")
    use_database(body.url)
    return {"ok": True, "url": mask_url(body.url)}


def use_database(url: str):
    global pool, DB_URL
    old = pool
    pool = ConnectionPool(url, min_size=1, max_size=8, open=True)
    DB_URL = url
    cfg = read_cfg()
    cfg["db_url_enc"] = _fernet().encrypt(url.encode()).decode()
    write_cfg(cfg)
    old.close()


from psycopg.types.json import Jsonb  # noqa: E402
JSONB_COLS = {"app_config": ("value",), "user_state": ("profile", "plan", "settings", "favs", "day", "history"), "submissions": ("recipe",)}
COPY_TABLES = [("admin_emails", "email"), ("users", "id"), ("user_state", "user_id"), ("weights", "user_id, d"),
               ("submissions", "id"), ("app_config", "key")]


class Connect(BaseModel):
    url: str = Field(default="", max_length=500)   # owner / admin connection string, or the separate fields below
    host: str = Field(default="", max_length=255)
    port: int = 5432
    database: str = Field(default="postgres", max_length=100)
    user: str = Field(default="postgres", max_length=100)
    password: str = Field(default="", max_length=200)
    copy_data: bool = True


def conn_url(body: "Connect") -> str:
    from urllib.parse import quote
    url = body.url.strip()
    if not url:
        if not (body.host and body.password):
            raise HTTPException(400, "Enter the host and the database password (or a full connection string)")
        url = f"postgresql://{quote(body.user, safe='')}:{quote(body.password, safe='')}@{body.host.strip()}:{body.port}/{quote(body.database, safe='')}?sslmode=require"
    check_url(url)
    return url


@app.post("/api/admin/database/connect")
def database_connect(body: Connect, user=Depends(admin)):
    """One step: set up the tables on the new database, create the restricted app user with a random password,
    copy the current accounts and data, then switch. The connection details are stored encrypted."""
    from urllib.parse import urlsplit, urlunsplit, quote
    body.url = conn_url(body)
    api_pw = secrets.token_urlsafe(24)
    copied = {}
    try:
        with psycopg.connect(body.url, connect_timeout=10, autocommit=True) as conn:
            conn.execute((HERE / "schema.sql").read_text())
            conn.execute(psycopg.sql.SQL("ALTER ROLE hk_api WITH LOGIN PASSWORD {}").format(psycopg.sql.Literal(api_pw)))
            if body.copy_data:
                with as_user(user["id"], "admin") as src:
                    for t, key in COPY_TABLES:
                        if t == "admin_emails":
                            continue   # read below through the owner-free path
                        rows = src.execute(f"SELECT * FROM hk.{t}").fetchall()
                        conn.execute(f"ALTER TABLE hk.{t} NO FORCE ROW LEVEL SECURITY")
                        conn.execute(f"ALTER TABLE hk.{t} DISABLE ROW LEVEL SECURITY")
                        try:
                            if rows:
                                cols = list(rows[0].keys())
                                with conn.cursor() as cur:
                                    cur.executemany(
                                        f"INSERT INTO hk.{t} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))}) ON CONFLICT ({key}) DO NOTHING",
                                        [[Jsonb(v) if c in JSONB_COLS.get(t, ()) else v for c, v in r.items()] for r in rows])
                            copied[t] = len(rows)
                        finally:
                            conn.execute(f"ALTER TABLE hk.{t} ENABLE ROW LEVEL SECURITY")
                            conn.execute(f"ALTER TABLE hk.{t} FORCE ROW LEVEL SECURITY")
                if copied.get("submissions"):
                    conn.execute("SELECT setval('hk.submissions_id_seq', (SELECT coalesce(max(id), 1) FROM hk.submissions))")
            parts = urlsplit(body.url)
            host = parts.hostname + (f":{parts.port}" if parts.port else "")
            api_url = urlunsplit((parts.scheme, f"hk_api:{quote(api_pw, safe='')}@{host}", parts.path, parts.query, ""))
        with psycopg.connect(api_url, connect_timeout=10) as test:
            test.execute("SELECT 1")
    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        raise HTTPException(400, f"Could not set up that database: {explain_db_error(e)}")
    use_database(api_url)
    return {"ok": True, "url": mask_url(api_url), "copied": copied}


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


@app.get("/favicon.ico")
def favicon():
    return FileResponse(GALLERY / "icon-32.png", media_type="image/png")


@app.get("/gallery")
@app.get("/gallery/")
def old_gallery_path():
    # links from the old static server (http://localhost:8099/gallery/#...) keep working; the #hash stays in the browser
    from fastapi.responses import RedirectResponse
    return RedirectResponse("/", status_code=307)


app.mount("/", StaticFiles(directory=GALLERY), name="gallery")
