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

DROP FUNCTION IF EXISTS hk.login_lookup(text);
CREATE FUNCTION hk.login_lookup(p_email text)
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

-- ---------- v2: disabled accounts, last seen, admin helpers ----------
ALTER TABLE hk.users ADD COLUMN IF NOT EXISTS disabled  boolean NOT NULL DEFAULT false;
ALTER TABLE hk.users ADD COLUMN IF NOT EXISTS last_seen timestamptz;

DROP FUNCTION IF EXISTS hk.login_lookup(text);
CREATE FUNCTION hk.login_lookup(p_email text)
RETURNS TABLE (id uuid, password_hash text, role text, name text, disabled boolean) LANGUAGE sql SECURITY DEFINER SET search_path = hk, pg_temp AS
$$ SELECT id, password_hash, role, name, disabled FROM hk.users WHERE email = lower(p_email) $$;

-- session lookup also refreshes last_seen (at most every 5 minutes) and ignores disabled accounts
CREATE OR REPLACE FUNCTION hk.session_user_of(p_token_hash text)
RETURNS TABLE (id uuid, role text) LANGUAGE plpgsql SECURITY DEFINER SET search_path = hk, pg_temp AS $$
DECLARE uid uuid; r text;
BEGIN
  SELECT u.id, u.role INTO uid, r FROM hk.sessions s JOIN hk.users u ON u.id = s.user_id
   WHERE s.token_hash = p_token_hash AND s.expires_at > now() AND NOT u.disabled;
  IF uid IS NULL THEN RETURN; END IF;
  UPDATE hk.users SET last_seen = now() WHERE users.id = uid AND (last_seen IS NULL OR last_seen < now() - interval '5 minutes');
  id := uid; role := r; RETURN NEXT;
END $$;

-- admins only: sign a user out everywhere (after a password reset or when disabling)
CREATE OR REPLACE FUNCTION hk.end_user_sessions(p_user uuid)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path = hk, pg_temp AS $$
BEGIN
  IF NOT hk.is_admin() THEN RAISE EXCEPTION 'admins only'; END IF;
  DELETE FROM hk.sessions WHERE user_id = p_user;
END $$;

GRANT EXECUTE ON FUNCTION hk.login_lookup(text), hk.session_user_of(text), hk.end_user_sessions(uuid) TO hk_api;
REVOKE EXECUTE ON FUNCTION hk.login_lookup(text), hk.session_user_of(text), hk.end_user_sessions(uuid) FROM PUBLIC;

-- ---------- v3: admins come only from hk.admin_emails ----------
CREATE TABLE IF NOT EXISTS hk.admin_emails (email text PRIMARY KEY CHECK (email = lower(email)));
INSERT INTO hk.admin_emails VALUES ('nmyamani@gmail.com') ON CONFLICT DO NOTHING;
REVOKE ALL ON hk.admin_emails FROM hk_api;

CREATE OR REPLACE FUNCTION hk.create_user(p_email text, p_hash text, p_name text)
RETURNS TABLE (id uuid, role text) LANGUAGE plpgsql SECURITY DEFINER SET search_path = hk, pg_temp AS $$
DECLARE r text := CASE WHEN EXISTS (SELECT 1 FROM hk.admin_emails a WHERE a.email = lower(p_email)) THEN 'admin' ELSE 'user' END;
BEGIN
  RETURN QUERY INSERT INTO hk.users (email, password_hash, name, role)
    VALUES (lower(p_email), p_hash, coalesce(p_name, ''), r) RETURNING users.id, users.role;
END $$;

-- roles: admin only for listed emails, whatever the API sends; an admin may make other users supervisors
ALTER TABLE hk.users DROP CONSTRAINT IF EXISTS users_role_check;
ALTER TABLE hk.users ADD CONSTRAINT users_role_check CHECK (role IN ('user', 'supervisor', 'admin'));
CREATE OR REPLACE FUNCTION hk.enforce_role() RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = hk, pg_temp AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM hk.admin_emails a WHERE a.email = NEW.email) THEN NEW.role := 'admin';
  ELSIF TG_OP = 'INSERT' OR NEW.role NOT IN ('user', 'supervisor') THEN NEW.role := 'user';
  ELSIF NEW.role IS DISTINCT FROM OLD.role AND NOT hk.is_admin() THEN NEW.role := OLD.role;
  END IF;
  RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS users_role ON hk.users;
CREATE TRIGGER users_role BEFORE INSERT OR UPDATE ON hk.users FOR EACH ROW EXECUTE FUNCTION hk.enforce_role();
UPDATE hk.users SET role = role;

-- ---------- v4: community recipes, published only after an admin approves them ----------
CREATE TABLE IF NOT EXISTS hk.submissions (
    id          serial PRIMARY KEY,
    user_id     uuid NOT NULL REFERENCES hk.users(id) ON DELETE CASCADE,
    recipe      jsonb NOT NULL,
    status      text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    admin_note  text NOT NULL DEFAULT '',
    created_at  timestamptz NOT NULL DEFAULT now(),
    reviewed_at timestamptz
);
ALTER TABLE hk.submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE hk.submissions FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS subs_read ON hk.submissions;
CREATE POLICY subs_read ON hk.submissions FOR SELECT USING (user_id = hk.current_user_id() OR hk.is_admin());
DROP POLICY IF EXISTS subs_insert ON hk.submissions;
CREATE POLICY subs_insert ON hk.submissions FOR INSERT WITH CHECK (user_id = hk.current_user_id() AND status = 'pending');
DROP POLICY IF EXISTS subs_update ON hk.submissions;
CREATE POLICY subs_update ON hk.submissions FOR UPDATE USING (hk.is_admin() OR (user_id = hk.current_user_id() AND status <> 'approved'))
    WITH CHECK (hk.is_admin() OR (user_id = hk.current_user_id() AND status = 'pending'));
DROP POLICY IF EXISTS subs_delete ON hk.submissions;
CREATE POLICY subs_delete ON hk.submissions FOR DELETE USING (hk.is_admin() OR (user_id = hk.current_user_id() AND status <> 'approved'));
GRANT SELECT, INSERT, UPDATE, DELETE ON hk.submissions TO hk_api;
GRANT USAGE ON SEQUENCE hk.submissions_id_seq TO hk_api;

-- approved recipes are public (recipe text and the author's first name only)
CREATE OR REPLACE FUNCTION hk.approved_recipes()
RETURNS TABLE (id int, recipe jsonb, author text, approved_at timestamptz) LANGUAGE sql STABLE SECURITY DEFINER SET search_path = hk, pg_temp AS
$$ SELECT s.id, s.recipe, split_part(u.name, ' ', 1), s.reviewed_at FROM hk.submissions s JOIN hk.users u ON u.id = s.user_id
   WHERE s.status = 'approved' ORDER BY s.reviewed_at $$;
GRANT EXECUTE ON FUNCTION hk.approved_recipes() TO hk_api;
REVOKE EXECUTE ON FUNCTION hk.approved_recipes() FROM PUBLIC;

-- ---------- v5: app settings managed from the Admin page ----------
CREATE TABLE IF NOT EXISTS hk.app_config (key text PRIMARY KEY, value jsonb NOT NULL, updated_at timestamptz NOT NULL DEFAULT now());
ALTER TABLE hk.app_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE hk.app_config FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS config_read ON hk.app_config;
CREATE POLICY config_read ON hk.app_config FOR SELECT USING (true);
DROP POLICY IF EXISTS config_write ON hk.app_config;
CREATE POLICY config_write ON hk.app_config FOR ALL USING (hk.is_admin()) WITH CHECK (hk.is_admin());
GRANT SELECT, INSERT, UPDATE, DELETE ON hk.app_config TO hk_api;
