create table if not exists public.hid_telemetry (
    id uuid primary key default gen_random_uuid(),
    endpoint_id uuid not null
        references public.endpoints(id)
        on delete cascade,

    device_id text not null,
    observation_window_ms integer not null,
    key_count integer not null,

    first_key_delay_ms integer,
    average_interval_ms numeric,
    interval_stddev_ms numeric,
    max_keys_per_second numeric not null default 0,

    risk_score integer not null default 0,
    risk_level text not null default 'info',
    risk_reasons jsonb not null default '[]'::jsonb,

    created_at timestamptz not null default now(),

    constraint hid_telemetry_key_count_check
        check (key_count >= 0),

    constraint hid_telemetry_window_check
        check (observation_window_ms > 0),

    constraint hid_telemetry_risk_score_check
        check (risk_score between 0 and 100),

    constraint hid_telemetry_risk_level_check
        check (
            risk_level in (
                'info',
                'low',
                'medium',
                'high',
                'critical'
            )
        )
);

create index if not exists hid_telemetry_endpoint_id_idx
on public.hid_telemetry(endpoint_id);

create index if not exists hid_telemetry_created_at_idx
on public.hid_telemetry(created_at desc);

alter table public.hid_telemetry enable row level security;

drop policy if exists "Users can view their HID telemetry"
on public.hid_telemetry;

create policy "Users can view their HID telemetry"
on public.hid_telemetry
for select
to authenticated
using (
    exists (
        select 1
        from public.endpoints
        where endpoints.id = hid_telemetry.endpoint_id
          and endpoints.user_id = auth.uid()
    )
);