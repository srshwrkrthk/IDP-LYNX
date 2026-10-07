import hashlib
import secrets
from datetime import datetime, timezone

from app.database import get_supabase_admin
from app.schemas.device import EndpointCreate, USBEventCreate


def register_endpoint(user_id: str, data: EndpointCreate):
    agent_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(agent_token.encode("utf-8")).hexdigest()

    response = (
        get_supabase_admin()
        .table("endpoints")
        .insert(
            {
                "user_id": user_id,
                "name": data.name,
                "hostname": data.hostname,
                "os_name": data.os_name,
                "agent_token_hash": token_hash,
            }
        )
        .execute()
    )

    if not response.data:
        raise RuntimeError("Endpoint registration failed")

    endpoint = response.data[0]
    endpoint.pop("agent_token_hash", None)

    return endpoint, agent_token


def list_endpoints(user_id: str):
    response = (
        get_supabase_admin()
        .table("endpoints")
        .select("id,name,hostname,os_name,status,last_seen,created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


def find_endpoint_by_token(agent_token: str):
    token_hash = hashlib.sha256(agent_token.encode("utf-8")).hexdigest()

    response = (
        get_supabase_admin()
        .table("endpoints")
        .select("id,user_id,name,status")
        .eq("agent_token_hash", token_hash)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def record_usb_event(endpoint_id: str, data: USBEventCreate):
    response = (
        get_supabase_admin()
        .table("usb_events")
        .insert(
            {
                "endpoint_id": endpoint_id,
                "event_type": data.event_type,
                "device_id": data.device_id,
                "device_name": data.device_name,
                "device_class": data.device_class,
                "vendor_id": data.vendor_id,
                "product_id": data.product_id,
                "serial_number": data.serial_number,
            }
        )
        .execute()
    )

    if not response.data:
        raise RuntimeError("USB event could not be stored")

    (
        get_supabase_admin()
        .table("endpoints")
        .update(
            {
                "status": "online",
                "last_seen": datetime.now(timezone.utc).isoformat(),
            }
        )
        .eq("id", endpoint_id)
        .execute()
    )

    return response.data[0]