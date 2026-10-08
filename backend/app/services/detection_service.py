from app.schemas.device import HIDTelemetryCreate, USBEventCreate

def get_risk_level(score: int) -> str:
    if score >= 80:
        return "critical"

    if score >= 60:
        return "high"

    if score >= 30:
        return "medium"

    if score > 0:
        return "low"

    return "info"


def assess_usb_event(data: USBEventCreate) -> dict:
    if data.event_type == "disconnected":
        return {
            "score": 0,
            "level": "info",
            "reasons": ["Device disconnected"],
        }

    score = 10
    reasons = ["New USB connection observed"]

    device_class = (data.device_class or "").lower()

    if any(item in device_class for item in ("hid", "keyboard", "mouse")):
        score += 15
        reasons.append("Device exposes HID capabilities")

    if "," in device_class:
        score += 10
        reasons.append("Device exposes multiple interfaces")

    if not data.vendor_id:
        score += 15
        reasons.append("Vendor identifier unavailable")

    if not data.product_id:
        score += 15
        reasons.append("Product identifier unavailable")

    if not data.serial_number:
        score += 10
        reasons.append("Device has no readable serial number")

    score = min(score, 100)

    return {
        "score": score,
        "level": get_risk_level(score),
        "reasons": reasons,
    }

def assess_hid_telemetry(data: HIDTelemetryCreate) -> dict:
    score = 0
    reasons = []

    if data.key_count == 0:
        return {
            "score": 0,
            "level": "info",
            "reasons": ["No keyboard activity observed"],
        }

    if data.key_count >= 40:
        score += 30
        reasons.append("High keystroke count during observation window")

    if data.max_keys_per_second >= 15:
        score += 30
        reasons.append("Typing burst exceeds normal human speed")

    if (
        data.first_key_delay_ms is not None
        and data.first_key_delay_ms <= 500
        and data.key_count >= 10
    ):
        score += 20
        reasons.append("Typing began immediately after HID connection")

    if (
        data.average_interval_ms is not None
        and data.average_interval_ms <= 50
        and data.key_count >= 10
    ):
        score += 20
        reasons.append("Average key interval indicates automated input")

    if (
        data.interval_stddev_ms is not None
        and data.interval_stddev_ms <= 12
        and data.key_count >= 10
    ):
        score += 20
        reasons.append("Highly consistent timing suggests scripted input")

    score = min(score, 100)

    if not reasons:
        reasons.append("No strong automation indicators detected")

    return {
        "score": score,
        "level": get_risk_level(score),
        "reasons": reasons,
    }