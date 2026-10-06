from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_current_user
from app.schemas.device import EndpointCreate
from app.services.device_service import list_endpoints, register_endpoint

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.schemas.device import EndpointCreate, USBEventCreate
from app.services.device_service import (
    find_endpoint_by_token,
    list_endpoints,
    record_usb_event,
    register_endpoint,
)

router = APIRouter(prefix="/endpoints", tags=["Endpoints"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_endpoint(
    data: EndpointCreate,
    current_user=Depends(get_current_user),
):
    endpoint, agent_token = register_endpoint(
        str(current_user.id),
        data,
    )

    return {
        "message": "Endpoint registered successfully",
        "endpoint": endpoint,
        "agent_token": agent_token,
        "warning": "Save this token now. It will not be shown again.",
    }

@router.post("/agent/events", status_code=status.HTTP_201_CREATED)
def receive_usb_event(
    data: USBEventCreate,
    agent_token: str = Header(alias="X-Agent-Token"),
):
    endpoint = find_endpoint_by_token(agent_token)

    if endpoint is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid agent token",
        )

    event = record_usb_event(endpoint["id"], data)

    return {
        "message": "USB event recorded",
        "event": event,
    }


@router.get("")
def get_endpoints(current_user=Depends(get_current_user)):
    return list_endpoints(str(current_user.id))