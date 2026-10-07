from app.database import get_supabase_admin


def list_user_events(user_id: str, limit: int = 50):
    client = get_supabase_admin()

    endpoint_response = (
        client
        .table("endpoints")
        .select("id,name")
        .eq("user_id", user_id)
        .execute()
    )

    endpoints = endpoint_response.data or []

    if not endpoints:
        return []

    endpoint_names = {
        endpoint["id"]: endpoint["name"]
        for endpoint in endpoints
    }

    endpoint_ids = list(endpoint_names.keys())

    event_response = (
        client
        .table("usb_events")
        .select(
            "id,endpoint_id,event_type,device_id,device_name,"
            "device_class,vendor_id,product_id,serial_number,"
            "risk_score,risk_level,risk_reasons,created_at"
        )
        .in_("endpoint_id", endpoint_ids)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    events = event_response.data or []

    for event in events:
        event["endpoint_name"] = endpoint_names.get(
            event["endpoint_id"],
            "Unknown endpoint",
        )

    return events