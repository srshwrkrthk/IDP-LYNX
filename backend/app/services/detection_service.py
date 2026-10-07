from app.schemas.device import USBEventCreate


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