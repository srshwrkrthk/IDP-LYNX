import re

import wmi


def extract_id(pattern: str, device_id: str) -> str | None:
    match = re.search(pattern, device_id, re.IGNORECASE)
    return match.group(1).upper() if match else None


def physical_key(device_id: str) -> str:
    vendor_id = extract_id(r"VID_([0-9A-F]{4})", device_id)
    product_id = extract_id(r"PID_([0-9A-F]{4})", device_id)

    if vendor_id and product_id:
        return f"{vendor_id}:{product_id}"

    return device_id


def choose_name(current_name: str, new_name: str) -> str:
    generic_terms = (
        "usb input device",
        "usb composite device",
        "hid-compliant",
        "hid keyboard device",
    )

    current_generic = current_name.lower().startswith(generic_terms)
    new_generic = new_name.lower().startswith(generic_terms)

    if current_generic and not new_generic:
        return new_name

    return current_name


def get_usb_devices() -> dict[str, dict]:
    connection = wmi.WMI()
    grouped = {}

    for device in connection.Win32_PnPEntity():
        device_id = device.PNPDeviceID or ""

        if not device_id.upper().startswith(("USB", "HID")):
            continue

        vendor_id = extract_id(r"VID_([0-9A-F]{4})", device_id)
        product_id = extract_id(r"PID_([0-9A-F]{4})", device_id)
        key = physical_key(device_id)

        name = device.Name or "Unknown USB Device"
        device_class = device.PNPClass or "Unknown"

        if key not in grouped:
            grouped[key] = {
                "device_id": key,
                "device_name": name,
                "device_class": {device_class},
                "vendor_id": vendor_id,
                "product_id": product_id,
                "serial_number": None,
            }
        else:
            grouped[key]["device_name"] = choose_name(
                grouped[key]["device_name"],
                name,
            )
            grouped[key]["device_class"].add(device_class)

    for device in grouped.values():
        device["device_class"] = ", ".join(
            sorted(device["device_class"])
        )

    return grouped