-- Admins can give any role (user, supervisor or admin) to other users. Emails in admin_emails always stay admin,
-- nobody can change their own role, and only admins can change roles at all. Safe to run more than once.

create or replace function public.protect_profile() returns trigger language plpgsql security definer set search_path = public as $$
begin
  if exists (select 1 from admin_emails a where a.email = new.email) then
    new.role := 'admin';
  elsif new.role is distinct from old.role and not public.is_admin() then
    new.role := old.role;
  elsif new.role not in ('user', 'supervisor', 'admin') then
    new.role := 'user';
  end if;
  if not public.is_admin() then
    new.email := old.email; new.disabled := old.disabled; new.created_at := old.created_at;
  end if;
  return new;
end $$;

-- admin: set another user's role
create or replace function public.admin_set_role(target uuid, new_role text) returns text language plpgsql security definer set search_path = public as $$
declare r text;
begin
  if not public.is_admin() then raise exception 'Admins only'; end if;
  if target = auth.uid() then raise exception 'You can''t change your own role'; end if;
  if new_role not in ('user', 'supervisor', 'admin') then raise exception 'Role must be user, supervisor or admin'; end if;
  update profiles set role = new_role where id = target returning role into r;
  if r is null then raise exception 'No such user'; end if;
  return r;
end $$;
revoke execute on function public.admin_set_role(uuid, text) from public, anon;
grant execute on function public.admin_set_role(uuid, text) to authenticated;
