import pytest
from pydantic import ValidationError

from app.schemas.device import USBEventCreate


def test_valid_usb_event():
    event = USBEventCreate(
        event_type="connected",
        device_id="USB\\VID_046D&PID_C534",
        device_name="USB Mouse",
        device_class="Mouse",
    )

    assert event.event_type == "connected"
    assert event.device_name == "USB Mouse"


def test_invalid_usb_event_type():
    with pytest.raises(ValidationError):
        USBEventCreate(
            event_type="unknown",
            device_id="test-device",
        )