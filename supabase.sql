-- ============================================================
--  Supabase — таблица заявок для сайта ХОЛОД-ОК
--  Выполнить один раз: Supabase -> SQL Editor -> New query -> вставить -> Run
-- ============================================================

create table if not exists public.leads (
  id          uuid primary key default gen_random_uuid(),
  created_at  timestamptz not null default now(),
  name        text default '',
  phone       text not null,
  message     text default '',
  source      text default 'Заявка с сайта',
  page        text default '',
  status      text not null default 'new',   -- new | work | done | cancel
  comment     text default '',
  utm         text default ''
);

-- индекс на дату (админка сортирует по ней)
create index if not exists leads_created_at_idx on public.leads (created_at desc);

-- ---------- RLS: доступ по анонимному ключу ----------
alter table public.leads enable row level security;

-- любой посетитель может ДОБАВИТЬ заявку
drop policy if exists "anon insert" on public.leads;
create policy "anon insert" on public.leads
  for insert to anon with check (true);

-- читать/менять/удалять может только сервисный ключ (админка ходит через него)
-- если хочешь, чтобы админка работала на анонимном ключе — раскомментируй ниже:
-- drop policy if exists "anon all" on public.leads;
-- create policy "anon all" on public.leads for all to anon using (true) with check (true);

-- сервисный ключ (service_role) обходит RLS автоматически
drop policy if exists "service all" on public.leads;
create policy "service all" on public.leads
  for all to service_role using (true) with check (true);
