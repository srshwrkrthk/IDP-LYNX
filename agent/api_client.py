import httpx

from agent.config import settings


def send_usb_event(event: dict) -> bool:
    url = f"{settings.lynx_api_url}/endpoints/agent/events"

    try:
        response = httpx.post(
            url,
            json=event,
            headers={"X-Agent-Token": settings.lynx_agent_token},
            timeout=10,
        )

        response.raise_for_status()
        return True

    except httpx.HTTPError as error:
        print(f"[API ERROR] {error}")
        return False

def send_hid_telemetry(telemetry: dict) -> bool:
    url = f"{settings.lynx_api_url}/endpoints/agent/hid-telemetry"

    try:
        response = httpx.post(
            url,
            json=telemetry,
            headers={"X-Agent-Token": settings.lynx_agent_token},
            timeout=10,
        )

        response.raise_for_status()
        return True

    except httpx.HTTPError as error:
        print(f"[HID API ERROR] {error}")
        return False