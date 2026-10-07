alter table public.usb_events
add column if not exists risk_score integer not null default 0;

alter table public.usb_events
add column if not exists risk_level text not null default 'info';

alter table public.usb_events
add column if not exists risk_reasons jsonb not null default '[]'::jsonb;

alter table public.usb_events
drop constraint if exists usb_events_risk_score_check;

alter table public.usb_events
add constraint usb_events_risk_score_check
check (risk_score between 0 and 100);

alter table public.usb_events
drop constraint if exists usb_events_risk_level_check;

alter table public.usb_events
add constraint usb_events_risk_level_check
check (risk_level in ('info', 'low', 'medium', 'high', 'critical'));