from app.schemas.device import HIDTelemetryCreate, USBEventCreate
from app.services.detection_service import (
    assess_hid_telemetry,
    assess_usb_event,
)


def test_unknown_hid_device_receives_risk_score():
    event = USBEventCreate(
        event_type="connected",
        device_id="unknown-device",
        device_name="Unknown HID Device",
        device_class="HIDClass, Keyboard",
    )

    result = assess_usb_event(event)

    assert result["score"] == 75
    assert result["level"] == "high"
    assert len(result["reasons"]) > 0


def test_disconnection_is_informational():
    event = USBEventCreate(
        event_type="disconnected",
        device_id="046D:C534",
        device_name="USB Receiver",
    )

    result = assess_usb_event(event)

    assert result["score"] == 0
    assert result["level"] == "info"

def test_rapid_hid_activity_is_critical():
    telemetry = HIDTelemetryCreate(
        device_id="046D:C534",
        observation_window_ms=5000,
        key_count=60,
        first_key_delay_ms=100,
        average_interval_ms=20,
        interval_stddev_ms=4,
        max_keys_per_second=25,
    )

    result = assess_hid_telemetry(telemetry)

    assert result["score"] == 100
    assert result["level"] == "critical"


def test_normal_hid_activity_is_informational():
    telemetry = HIDTelemetryCreate(
        device_id="046D:C534",
        observation_window_ms=5000,
        key_count=8,
        first_key_delay_ms=1200,
        average_interval_ms=180,
        interval_stddev_ms=70,
        max_keys_per_second=4,
    )

    result = assess_hid_telemetry(telemetry)

    assert result["score"] == 0
    assert result["level"] == "info"