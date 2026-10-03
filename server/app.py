#!/usr/bin/env python3
"""Health Kitchen API: accounts, per-user state and admin, on a local PostgreSQL.

Serves the gallery (../gallery) at / and the API under /api. Every request that touches
user data runs in a transaction with hk.user_id / hk.role set, so PostgreSQL row-level
security limits it to that user's rows (admins see all).

Run:  server/run.sh   (or: uvicorn app:app --host 0.0.0.0 --port 8099 from server/)
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
DB_URL = os.environ.get("HK_DB_URL", "postgresql://hk_api:hk_api_dev_pw@127.0.0.1:5440/health_kitchen")
SESSION_DAYS = 30
pool = ConnectionPool(DB_URL, min_size=1, max_size=8, open=True)
app = FastAPI(title="Health Kitchen API")


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


def new_session(c, uid):
    tok = secrets.token_urlsafe(32)
    c.execute("SELECT hk.start_session(%s, %s, %s)", (uid, token_hash(tok), SESSION_DAYS))
    return tok


@app.post("/api/signup")
def signup(body: SignUp):
    if not EMAIL_RE.match(body.email):
        raise HTTPException(400, "Enter a valid email address")
    with as_user() as c:
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
@app.get("/api/admin/users")
def admin_users(user=Depends(admin)):
    with as_user(user["id"], "admin") as c:
        rows = c.execute("""SELECT u.id, u.email, u.name, u.role, u.created_at, u.last_login,
                                   s.plan->>'type' AS plan_type, jsonb_array_length(coalesce(s.favs, '[]')) AS saved,
                                   (SELECT count(*) FROM hk.weights w WHERE w.user_id = u.id) AS weigh_ins,
                                   (SELECT kg FROM hk.weights w WHERE w.user_id = u.id ORDER BY d DESC LIMIT 1) AS last_kg,
                                   s.updated_at
                            FROM hk.users u LEFT JOIN hk.user_state s ON s.user_id = u.id ORDER BY u.created_at""").fetchall()
    return {"users": [{**r, "last_kg": float(r["last_kg"]) if r["last_kg"] is not None else None} for r in rows]}


class RoleChange(BaseModel):
    role: str


@app.put("/api/admin/users/{uid}/role")
def admin_role(uid: str, body: RoleChange, user=Depends(admin)):
    if body.role not in ("user", "admin"):
        raise HTTPException(400, "Unknown role")
    with as_user(user["id"], "admin") as c:
        c.execute("UPDATE hk.users SET role = %s WHERE id = %s", (body.role, uid))
    return {"ok": True}


@app.delete("/api/admin/users/{uid}")
def admin_delete(uid: str, user=Depends(admin)):
    if uid == str(user["id"]):
        raise HTTPException(400, "You can't delete your own account here")
    with as_user(user["id"], "admin") as c:
        c.execute("DELETE FROM hk.users WHERE id = %s", (uid,))
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


app.mount("/", StaticFiles(directory=GALLERY), name="gallery")
