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

class HIDTelemetryCreate(BaseModel):
    device_id: str = Field(min_length=1)
    observation_window_ms: int = Field(gt=0)
    key_count: int = Field(ge=0)

    first_key_delay_ms: int | None = Field(default=None, ge=0)
    average_interval_ms: float | None = Field(default=None, ge=0)
    interval_stddev_ms: float | None = Field(default=None, ge=0)
    max_keys_per_second: float = Field(default=0, ge=0)