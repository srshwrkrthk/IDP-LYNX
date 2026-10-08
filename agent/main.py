import time

from agent.api_client import send_hid_telemetry, send_usb_event
from agent.config import settings
from agent.hid_monitor import HIDMonitor
from agent.usb_monitor import get_usb_devices


def supports_keyboard_input(device: dict) -> bool:
    device_class = (device.get("device_class") or "").lower()

    return any(
        value in device_class
        for value in ("hid", "keyboard")
    )


def main():
    print("LYNX Windows Agent")
    print("Monitoring USB and HID devices...")

    hid_monitor = HIDMonitor()
    hid_monitor.start()

    previous = get_usb_devices()
    pending_observations = {}

    print(f"Baseline created with {len(previous)} physical devices")

    try:
        while True:
            current = get_usb_devices()
            now = time.monotonic()

            connected = current.keys() - previous.keys()
            disconnected = previous.keys() - current.keys()

            for device_id in connected:
                device = current[device_id]

                event = {
                    "event_type": "connected",
                    **device,
                }

                if send_usb_event(event):
                    print(f"[CONNECTED] {event['device_name']}")

                if supports_keyboard_input(device):
                    pending_observations[device_id] = now
                    print(
                        f"[HID] Observing {device['device_name']} "
                        f"for {settings.lynx_hid_window_seconds} seconds"
                    )

            for device_id in disconnected:
                device = previous[device_id]

                event = {
                    "event_type": "disconnected",
                    **device,
                }

                if send_usb_event(event):
                    print(f"[DISCONNECTED] {event['device_name']}")

                pending_observations.pop(device_id, None)

            completed = [
                device_id
                for device_id, started_at in pending_observations.items()
                if now - started_at >= settings.lynx_hid_window_seconds
            ]

            for device_id in completed:
                started_at = pending_observations.pop(device_id)

                telemetry = hid_monitor.summarize(
                    device_id=device_id,
                    started_at=started_at,
                    ended_at=now,
                )

                if send_hid_telemetry(telemetry):
                    print(
                        f"[HID ANALYSED] {device_id} — "
                        f"{telemetry['key_count']} key events"
                    )

            previous = current
            time.sleep(settings.lynx_poll_interval)

    except KeyboardInterrupt:
        print("\nLYNX agent stopped")

    finally:
        hid_monitor.stop()


if __name__ == "__main__":
    main()