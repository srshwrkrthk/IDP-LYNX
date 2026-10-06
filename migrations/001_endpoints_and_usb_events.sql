create table public.endpoints (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    name text not null,
    hostname text not null,
    os_name text not null,
    status text not null default 'offline',
    created_at timestamptz not null default now()
);

create table public.usb_events (
    id uuid primary key default gen_random_uuid(),
    endpoint_id uuid not null references public.endpoints(id) on delete cascade,
    event_type text not null,
    device_id text not null,
    device_name text,
    device_class text,
    vendor_id text,
    product_id text,
    serial_number text,
    created_at timestamptz not null default now()
);

create index endpoints_user_id_idx
on public.endpoints(user_id);

create index usb_events_endpoint_id_idx
on public.usb_events(endpoint_id);