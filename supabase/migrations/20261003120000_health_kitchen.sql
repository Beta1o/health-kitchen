-- Health Kitchen on Supabase (free tier): accounts, per-user data, recipe submissions and app settings.
-- Sign-in uses Supabase Auth (email + password). Every table has row-level security: a user reads and
-- writes only their own rows; admins (emails listed in admin_emails) can read all and manage the app.
-- Safe to run more than once.

create table if not exists public.admin_emails (email text primary key check (email = lower(email)));
insert into public.admin_emails values ('nmyamani@gmail.com') on conflict do nothing;
alter table public.admin_emails enable row level security;   -- no policies: not readable from the app

create table if not exists public.profiles (
  id         uuid primary key references auth.users (id) on delete cascade,
  email      text not null,
  name       text not null default '',
  role       text not null default 'user' check (role in ('user', 'admin')),
  disabled   boolean not null default false,
  created_at timestamptz not null default now(),
  last_seen  timestamptz
);

create table if not exists public.user_state (
  user_id    uuid primary key references public.profiles (id) on delete cascade,
  profile    jsonb not null default '{}',
  plan       jsonb not null default '{}',
  settings   jsonb not null default '{}',
  favs       jsonb not null default '[]',
  day        jsonb not null default '[]',
  day_date   date,
  history    jsonb not null default '{}',
  updated_at timestamptz not null default now()
);

create table if not exists public.weights (
  user_id uuid not null references public.profiles (id) on delete cascade,
  d       date not null,
  kg      numeric(5, 1) not null check (kg > 20 and kg < 400),
  primary key (user_id, d)
);

create table if not exists public.submissions (
  id          bigserial primary key,
  user_id     uuid not null references public.profiles (id) on delete cascade,
  recipe      jsonb not null,
  status      text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  admin_note  text not null default '',
  created_at  timestamptz not null default now(),
  reviewed_at timestamptz
);

create table if not exists public.app_config (key text primary key, value jsonb not null, updated_at timestamptz not null default now());

-- ---------- helpers ----------
create or replace function public.is_admin() returns boolean language sql stable security definer set search_path = public as
$$ select exists (select 1 from profiles p where p.id = auth.uid() and p.role = 'admin' and not p.disabled) $$;
create or replace function public.is_active() returns boolean language sql stable security definer set search_path = public as
$$ select exists (select 1 from profiles p where p.id = auth.uid() and not p.disabled) $$;

-- a profile is created with every new account; the role comes only from admin_emails
create or replace function public.handle_new_user() returns trigger language plpgsql security definer set search_path = public as $$
declare open boolean := coalesce((select (value)::text::boolean from app_config where key = 'allow_signups'), true);
begin
  if not open and not exists (select 1 from admin_emails a where a.email = lower(new.email)) then
    raise exception 'New sign-ups are closed';
  end if;
  insert into profiles (id, email, name, role)
  values (new.id, lower(new.email), coalesce(new.raw_user_meta_data ->> 'name', ''),
          case when exists (select 1 from admin_emails a where a.email = lower(new.email)) then 'admin' else 'user' end)
  on conflict (id) do nothing;
  insert into user_state (user_id) values (new.id) on conflict do nothing;
  return new;
end $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users for each row execute function public.handle_new_user();

-- users can change only their name; role, email and disabled are protected
create or replace function public.protect_profile() returns trigger language plpgsql security definer set search_path = public as $$
begin
  new.role := case when exists (select 1 from admin_emails a where a.email = new.email) then 'admin' else 'user' end;
  if not public.is_admin() then
    new.email := old.email; new.disabled := old.disabled; new.created_at := old.created_at;
  end if;
  return new;
end $$;
drop trigger if exists profiles_protect on public.profiles;
create trigger profiles_protect before update on public.profiles for each row execute function public.protect_profile();

-- ---------- row-level security ----------
alter table public.profiles    enable row level security;
alter table public.user_state  enable row level security;
alter table public.weights     enable row level security;
alter table public.submissions enable row level security;
alter table public.app_config  enable row level security;

drop policy if exists profiles_read on public.profiles;
create policy profiles_read on public.profiles for select using (id = auth.uid() or public.is_admin());
drop policy if exists profiles_update on public.profiles;
create policy profiles_update on public.profiles for update using (id = auth.uid() or public.is_admin());
drop policy if exists profiles_delete on public.profiles;
create policy profiles_delete on public.profiles for delete using (public.is_admin() and id <> auth.uid());

drop policy if exists state_own on public.user_state;
create policy state_own on public.user_state for all using ((user_id = auth.uid() and public.is_active()) or public.is_admin())
  with check (user_id = auth.uid() and public.is_active());
drop policy if exists weights_own on public.weights;
create policy weights_own on public.weights for all using ((user_id = auth.uid() and public.is_active()) or public.is_admin())
  with check (user_id = auth.uid() and public.is_active());

drop policy if exists subs_read on public.submissions;
create policy subs_read on public.submissions for select using (user_id = auth.uid() or public.is_admin());
drop policy if exists subs_insert on public.submissions;
create policy subs_insert on public.submissions for insert with check (user_id = auth.uid() and status = 'pending' and public.is_active());
drop policy if exists subs_update on public.submissions;
create policy subs_update on public.submissions for update using (public.is_admin());
drop policy if exists subs_delete on public.submissions;
create policy subs_delete on public.submissions for delete using (public.is_admin() or (user_id = auth.uid() and status <> 'approved'));

drop policy if exists config_read on public.app_config;
create policy config_read on public.app_config for select using (true);
drop policy if exists config_write on public.app_config;
create policy config_write on public.app_config for all using (public.is_admin()) with check (public.is_admin());

-- ---------- functions the app calls ----------
-- approved community recipes are public (recipe text and the author's first name only)
create or replace function public.approved_recipes() returns table (id bigint, recipe jsonb, author text, approved_at timestamptz)
language sql stable security definer set search_path = public as
$$ select s.id, s.recipe, split_part(p.name, ' ', 1), s.reviewed_at from submissions s join profiles p on p.id = s.user_id
   where s.status = 'approved' order by s.reviewed_at $$;

-- admin overview: users with their plan and activity, and sign-ups per day
create or replace function public.admin_users() returns table (id uuid, email text, name text, role text, disabled boolean, created_at timestamptz,
  last_seen timestamptz, plan_type text, saved int, weigh_ins bigint, last_kg numeric, updated_at timestamptz)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'Admins only'; end if;
  return query select p.id, p.email, p.name, p.role, p.disabled, p.created_at, p.last_seen, s.plan ->> 'type',
    jsonb_array_length(coalesce(s.favs, '[]')), (select count(*) from weights w where w.user_id = p.id),
    (select w.kg from weights w where w.user_id = p.id order by w.d desc limit 1), s.updated_at
  from profiles p left join user_state s on s.user_id = p.id order by p.created_at;
end $$;

create or replace function public.admin_stats() returns jsonb language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'Admins only'; end if;
  return jsonb_build_object(
    'users', (select count(*) from profiles), 'admins', (select count(*) from profiles where role = 'admin'),
    'disabled', (select count(*) from profiles where disabled),
    'active_day', (select count(*) from profiles where last_seen > now() - interval '1 day'),
    'active_week', (select count(*) from profiles where last_seen > now() - interval '7 days'),
    'weigh_ins', (select count(*) from weights),
    'signups', (select jsonb_agg(jsonb_build_object('d', to_char(d, 'YYYY-MM-DD'), 'n', (select count(*) from profiles p where p.created_at::date = d::date)) order by d)
                from generate_series(current_date - 29, current_date, interval '1 day') d));
end $$;

create or replace function public.touch_last_seen() returns void language sql security definer set search_path = public as
$$ update profiles set last_seen = now() where id = auth.uid() and (last_seen is null or last_seen < now() - interval '5 minutes') $$;

grant execute on function public.approved_recipes() to anon, authenticated;
grant execute on function public.admin_users(), public.admin_stats(), public.touch_last_seen(), public.is_admin(), public.is_active() to authenticated;
