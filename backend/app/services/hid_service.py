from app.database import get_supabase_admin
from app.schemas.device import HIDTelemetryCreate
from app.services.detection_service import assess_hid_telemetry


def record_hid_telemetry(
    endpoint_id: str,
    data: HIDTelemetryCreate,
):
    assessment = assess_hid_telemetry(data)

    response = (
        get_supabase_admin()
        .table("hid_telemetry")
        .insert(
            {
                "endpoint_id": endpoint_id,
                "device_id": data.device_id,
                "observation_window_ms": data.observation_window_ms,
                "key_count": data.key_count,
                "first_key_delay_ms": data.first_key_delay_ms,
                "average_interval_ms": data.average_interval_ms,
                "interval_stddev_ms": data.interval_stddev_ms,
                "max_keys_per_second": data.max_keys_per_second,
                "risk_score": assessment["score"],
                "risk_level": assessment["level"],
                "risk_reasons": assessment["reasons"],
            }
        )
        .execute()
    )

    if not response.data:
        raise RuntimeError("HID telemetry could not be stored")

    return response.data[0]