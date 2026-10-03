-- Health Kitchen accounts: users, sessions, per-user state and weight log.
-- Row-level security: the API connects as hk_api (no superuser, no BYPASSRLS) and sets
-- hk.user_id / hk.role for each request, so every query only sees that user's rows
-- (admins see all). Sign-up, login and session lookup go through SECURITY DEFINER
-- functions, the only way to read accounts without a signed-in user.

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS hk;

CREATE TABLE IF NOT EXISTS hk.users (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email         text NOT NULL UNIQUE CHECK (email = lower(email)),
    password_hash text NOT NULL,
    name          text NOT NULL DEFAULT '',
    role          text NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    created_at    timestamptz NOT NULL DEFAULT now(),
    last_login    timestamptz
);

CREATE TABLE IF NOT EXISTS hk.sessions (
    token_hash text PRIMARY KEY,
    user_id    uuid NOT NULL REFERENCES hk.users(id) ON DELETE CASCADE,
    created_at timestamptz NOT NULL DEFAULT now(),
    expires_at timestamptz NOT NULL
);

-- everything the app keeps per user: profile, health plan, settings, saved recipes, today, history
CREATE TABLE IF NOT EXISTS hk.user_state (
    user_id    uuid PRIMARY KEY REFERENCES hk.users(id) ON DELETE CASCADE,
    profile    jsonb NOT NULL DEFAULT '{}',
    plan       jsonb NOT NULL DEFAULT '{}',
    settings   jsonb NOT NULL DEFAULT '{}',
    favs       jsonb NOT NULL DEFAULT '[]',
    day        jsonb NOT NULL DEFAULT '[]',
    day_date   date,
    history    jsonb NOT NULL DEFAULT '{}',
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS hk.weights (
    user_id uuid NOT NULL REFERENCES hk.users(id) ON DELETE CASCADE,
    d       date NOT NULL,
    kg      numeric(5, 1) NOT NULL CHECK (kg > 20 AND kg < 400),
    PRIMARY KEY (user_id, d)
);

-- ---------- row-level security ----------
CREATE OR REPLACE FUNCTION hk.current_user_id() RETURNS uuid LANGUAGE sql STABLE AS
$$ SELECT nullif(current_setting('hk.user_id', true), '')::uuid $$;
CREATE OR REPLACE FUNCTION hk.is_admin() RETURNS boolean LANGUAGE sql STABLE AS
$$ SELECT coalesce(current_setting('hk.role', true), '') = 'admin' $$;

ALTER TABLE hk.users      ENABLE ROW LEVEL SECURITY;
ALTER TABLE hk.user_state ENABLE ROW LEVEL SECURITY;
ALTER TABLE hk.weights    ENABLE ROW LEVEL SECURITY;
ALTER TABLE hk.sessions   ENABLE ROW LEVEL SECURITY;
ALTER TABLE hk.users      FORCE ROW LEVEL SECURITY;
ALTER TABLE hk.user_state FORCE ROW LEVEL SECURITY;
ALTER TABLE hk.weights    FORCE ROW LEVEL SECURITY;
ALTER TABLE hk.sessions   FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS users_self ON hk.users;
CREATE POLICY users_self ON hk.users USING (id = hk.current_user_id() OR hk.is_admin())
    WITH CHECK (id = hk.current_user_id() OR hk.is_admin());
DROP POLICY IF EXISTS state_self ON hk.user_state;
CREATE POLICY state_self ON hk.user_state USING (user_id = hk.current_user_id() OR hk.is_admin())
    WITH CHECK (user_id = hk.current_user_id());
DROP POLICY IF EXISTS weights_self ON hk.weights;
CREATE POLICY weights_self ON hk.weights USING (user_id = hk.current_user_id() OR hk.is_admin())
    WITH CHECK (user_id = hk.current_user_id());
DROP POLICY IF EXISTS sessions_self ON hk.sessions;
CREATE POLICY sessions_self ON hk.sessions USING (user_id = hk.current_user_id());

-- ---------- account functions (run as owner, narrowly scoped) ----------
-- first account becomes the admin
CREATE OR REPLACE FUNCTION hk.create_user(p_email text, p_hash text, p_name text)
RETURNS TABLE (id uuid, role text) LANGUAGE plpgsql SECURITY DEFINER SET search_path = hk, pg_temp AS $$
DECLARE r text := CASE WHEN EXISTS (SELECT 1 FROM hk.users) THEN 'user' ELSE 'admin' END;
BEGIN
  RETURN QUERY INSERT INTO hk.users (email, password_hash, name, role)
    VALUES (lower(p_email), p_hash, coalesce(p_name, ''), r) RETURNING users.id, users.role;
END $$;

CREATE OR REPLACE FUNCTION hk.login_lookup(p_email text)
RETURNS TABLE (id uuid, password_hash text, role text, name text) LANGUAGE sql SECURITY DEFINER SET search_path = hk, pg_temp AS
$$ SELECT id, password_hash, role, name FROM hk.users WHERE email = lower(p_email) $$;

CREATE OR REPLACE FUNCTION hk.start_session(p_user uuid, p_token_hash text, p_days int)
RETURNS void LANGUAGE sql SECURITY DEFINER SET search_path = hk, pg_temp AS $$
  INSERT INTO hk.sessions (token_hash, user_id, expires_at) VALUES (p_token_hash, p_user, now() + make_interval(days => p_days));
  UPDATE hk.users SET last_login = now() WHERE id = p_user;
  DELETE FROM hk.sessions WHERE expires_at < now();
$$;

CREATE OR REPLACE FUNCTION hk.session_user_of(p_token_hash text)
RETURNS TABLE (id uuid, role text) LANGUAGE sql SECURITY DEFINER SET search_path = hk, pg_temp AS
$$ SELECT u.id, u.role FROM hk.sessions s JOIN hk.users u ON u.id = s.user_id
   WHERE s.token_hash = p_token_hash AND s.expires_at > now() $$;

CREATE OR REPLACE FUNCTION hk.end_session(p_token_hash text)
RETURNS void LANGUAGE sql SECURITY DEFINER SET search_path = hk, pg_temp AS
$$ DELETE FROM hk.sessions WHERE token_hash = p_token_hash $$;

-- ---------- API role ----------
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'hk_api') THEN
    CREATE ROLE hk_api LOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE;
  END IF;
END $$;
GRANT USAGE ON SCHEMA hk TO hk_api;
GRANT SELECT, UPDATE ON hk.users TO hk_api;
GRANT DELETE ON hk.users TO hk_api;
GRANT SELECT, INSERT, UPDATE, DELETE ON hk.user_state, hk.weights TO hk_api;
REVOKE ALL ON hk.sessions FROM hk_api;
GRANT EXECUTE ON FUNCTION hk.create_user(text, text, text), hk.login_lookup(text), hk.start_session(uuid, text, int),
    hk.session_user_of(text), hk.end_session(text), hk.current_user_id(), hk.is_admin() TO hk_api;
REVOKE EXECUTE ON FUNCTION hk.create_user(text, text, text), hk.login_lookup(text), hk.start_session(uuid, text, int),
    hk.session_user_of(text), hk.end_session(text) FROM PUBLIC;
