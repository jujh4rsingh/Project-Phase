from datetime import datetime

from pydantic import BaseModel


class DeviceStatus(BaseModel):
    device_id: str
    name: str
    connected: bool
    battery_percent: int | None = None
    last_seen: datetime
    data_quality: str
    sensors: list[str]


class SensorReading(BaseModel):
    timestamp: datetime
    temperature: float
    humidity: float
    pm25: float
    pm10: float
    co2: float
    voc: float
    uv: float
    data_quality: str
