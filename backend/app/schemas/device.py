from typing import Literal

from pydantic import BaseModel, Field


class EndpointCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    hostname: str = Field(min_length=1, max_length=255)
    os_name: str = Field(min_length=1, max_length=100)


class USBEventCreate(BaseModel):
    event_type: Literal["connected", "disconnected"]
    device_id: str
    device_name: str | None = None
    device_class: str | None = None
    vendor_id: str | None = None
    product_id: str | None = None
    serial_number: str | None = None