from datetime import datetime

from pydantic import BaseModel


class ExposureSummary(BaseModel):
    date: str
    outdoor_minutes: int
    high_uv_minutes: int
    elevated_pollution_minutes: int
    highest_exposure_period: str
    transport_context: str
    indoor_air_quality: str
    source: str


class ExposureEvent(BaseModel):
    timestamp: datetime
    duration_minutes: int
    context: str
    uv_status: str
    pollution_status: str
