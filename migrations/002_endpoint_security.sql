alter table public.endpoints
add column if not exists agent_token_hash text;

alter table public.endpoints
add column if not exists last_seen timestamptz;

alter table public.endpoints
alter column agent_token_hash set not null;

create unique index if not exists endpoints_agent_token_hash_idx
on public.endpoints(agent_token_hash);

alter table public.endpoints
drop constraint if exists endpoints_status_check;

alter table public.endpoints
add constraint endpoints_status_check
check (status in ('online', 'offline'));

alter table public.usb_events
drop constraint if exists usb_events_event_type_check;

alter table public.usb_events
add constraint usb_events_event_type_check
check (event_type in ('connected', 'disconnected'));

alter table public.endpoints enable row level security;
alter table public.usb_events enable row level security;

drop policy if exists "Users can view their endpoints"
on public.endpoints;

create policy "Users can view their endpoints"
on public.endpoints
for select
to authenticated
using (auth.uid() = user_id);

drop policy if exists "Users can view their USB events"
on public.usb_events;

create policy "Users can view their USB events"
on public.usb_events
for select
to authenticated
using (
    exists (
        select 1
        from public.endpoints
        where endpoints.id = usb_events.endpoint_id
          and endpoints.user_id = auth.uid()
    )
);