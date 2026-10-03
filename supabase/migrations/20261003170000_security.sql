-- Health Kitchen security update (safe to run more than once). Paste ALL of this into Supabase → SQL Editor → Run.
-- 1) Supervisor role set by admins  2) append-only audit log of admin actions  3) size and shape limits on stored data
-- 4) admin functions callable only by signed-in users (and they check for admin inside).

alter table public.profiles drop constraint if exists profiles_role_check;
alter table public.profiles add constraint profiles_role_check check (role in ('user', 'supervisor', 'admin'));

create or replace function public.protect_profile() returns trigger language plpgsql security definer set search_path = public as $$
begin
  if exists (select 1 from admin_emails a where a.email = new.email) then
    new.role := 'admin';
  elsif new.role is distinct from old.role and not public.is_admin() then
    new.role := old.role;
  elsif new.role not in ('user', 'supervisor') then
    new.role := 'user';
  end if;
  if not public.is_admin() then
    new.email := old.email; new.disabled := old.disabled; new.created_at := old.created_at;
  end if;
  return new;
end $$;

-- admin: set a user's role (not their own)
create or replace function public.admin_set_role(target uuid, new_role text) returns text language plpgsql security definer set search_path = public as $$
declare r text;
begin
  if not public.is_admin() then raise exception 'Admins only'; end if;
  if target = auth.uid() then raise exception 'You can''t change your own role'; end if;
  if new_role not in ('user', 'supervisor') then raise exception 'Role must be user or supervisor'; end if;
  update profiles set role = new_role where id = target returning role into r;
  if r is null then raise exception 'No such user'; end if;
  return r;
end $$;
grant execute on function public.admin_set_role(uuid, text) to authenticated;

-- ---------- audit log: written only by the triggers below, read only by admins ----------
create table if not exists public.audit_log (
  id     bigserial primary key,
  at     timestamptz not null default now(),
  actor  uuid,
  action text not null,
  target text not null default '',
  detail jsonb not null default '{}'
);
alter table public.audit_log enable row level security;
drop policy if exists audit_read on public.audit_log;
create policy audit_read on public.audit_log for select using (public.is_admin());
revoke insert, update, delete on public.audit_log from anon, authenticated;

create or replace function public.audit_profiles() returns trigger language plpgsql security definer set search_path = public as $$
begin
  if tg_op = 'DELETE' then
    insert into audit_log (actor, action, target, detail) values (auth.uid(), 'user_deleted', old.id::text, jsonb_build_object('email', old.email));
    return old;
  end if;
  if new.role is distinct from old.role then
    insert into audit_log (actor, action, target, detail) values (auth.uid(), 'role_changed', new.id::text, jsonb_build_object('email', new.email, 'role', new.role));
  end if;
  if new.disabled is distinct from old.disabled then
    insert into audit_log (actor, action, target, detail)
    values (auth.uid(), case when new.disabled then 'user_disabled' else 'user_enabled' end, new.id::text, jsonb_build_object('email', new.email));
  end if;
  return new;
end $$;
drop trigger if exists profiles_audit on public.profiles;
create trigger profiles_audit after update or delete on public.profiles for each row execute function public.audit_profiles();

create or replace function public.audit_config() returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into audit_log (actor, action, target) values (auth.uid(), 'settings_changed', new.key);
  return new;
end $$;
drop trigger if exists app_config_audit on public.app_config;
create trigger app_config_audit after insert or update on public.app_config for each row execute function public.audit_config();

create or replace function public.admin_audit() returns table (at timestamptz, action text, target text, detail jsonb, actor_email text, target_label text)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'Admins only'; end if;
  return query select a.at, a.action, a.target, a.detail, coalesce(p.email, ''), coalesce(t.email, a.detail ->> 'email', a.target)
    from audit_log a left join profiles p on p.id = a.actor left join profiles t on t.id::text = a.target
    order by a.id desc limit 200;
end $$;

-- ---------- limits on stored data (stops oversized or malformed rows) ----------
alter table public.submissions drop constraint if exists submissions_recipe_shape;
alter table public.submissions add constraint submissions_recipe_shape check (jsonb_typeof(recipe) = 'object' and pg_column_size(recipe) < 65536);
alter table public.submissions drop constraint if exists submissions_note_len;
alter table public.submissions add constraint submissions_note_len check (length(admin_note) <= 1000);
alter table public.profiles drop constraint if exists profiles_name_len;
alter table public.profiles add constraint profiles_name_len check (length(name) <= 100);
alter table public.user_state drop constraint if exists user_state_size;
alter table public.user_state add constraint user_state_size check (
  pg_column_size(profile) + pg_column_size(plan) + pg_column_size(settings) + pg_column_size(favs) + pg_column_size(day) + pg_column_size(history) < 2000000);
alter table public.app_config drop constraint if exists app_config_size;
alter table public.app_config add constraint app_config_size check (pg_column_size(value) < 100000);

-- ---------- who may call the functions ----------
revoke execute on function public.admin_users(), public.admin_stats(), public.admin_set_role(uuid, text), public.admin_audit() from public, anon;
grant execute on function public.admin_users(), public.admin_stats(), public.admin_set_role(uuid, text), public.admin_audit() to authenticated;
revoke execute on function public.touch_last_seen() from public, anon;
grant execute on function public.touch_last_seen() to authenticated;
