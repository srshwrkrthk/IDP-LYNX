from app.schemas.device import USBEventCreate
from app.services.detection_service import assess_usb_event


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