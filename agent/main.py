import time

from agent.api_client import send_usb_event
from agent.config import settings
from agent.usb_monitor import get_usb_devices


def main():
    print("LYNX Windows Agent")
    print("Monitoring USB and HID devices...")

    previous = get_usb_devices()
    print(f"Baseline created with {len(previous)} device interfaces")

    while True:
        try:
            current = get_usb_devices()

            connected = current.keys() - previous.keys()
            disconnected = previous.keys() - current.keys()

            for device_id in connected:
                event = {
                    "event_type": "connected",
                    **current[device_id],
                }

                if send_usb_event(event):
                    print(f"[CONNECTED] {event['device_name']}")

            for device_id in disconnected:
                event = {
                    "event_type": "disconnected",
                    **previous[device_id],
                }

                if send_usb_event(event):
                    print(f"[DISCONNECTED] {event['device_name']}")

            previous = current
            time.sleep(settings.lynx_poll_interval)

        except KeyboardInterrupt:
            print("\nLYNX agent stopped")
            break

        except Exception as error:
            print(f"[AGENT ERROR] {error}")
            time.sleep(settings.lynx_poll_interval)


if __name__ == "__main__":
    main()