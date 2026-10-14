from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class DataQuality(StrEnum):
    LIVE = "LIVE"
    RECENT = "RECENT"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"
    SIMULATED = "SIMULATED"


class EnvironmentSnapshot(BaseModel):
    timestamp: datetime
    source: str
    environment_type: str = "OUTDOOR"
    temperature: float | None = None
    humidity: float | None = Field(default=None, ge=0, le=100)
    apparent_temperature: float | None = None
    uv_index: float | None = Field(default=None, ge=0)
    pm25: float | None = Field(default=None, ge=0)
    pm10: float | None = Field(default=None, ge=0)
    aqi: float | None = Field(default=None, ge=0)
    wind_speed: float | None = Field(default=None, ge=0)
    cloud_cover: float | None = Field(default=None, ge=0, le=100)
    precipitation: float | None = Field(default=None, ge=0)
    solar_radiation: float | None = Field(default=None, ge=0)
    ozone: float | None = Field(default=None, ge=0)
    no2: float | None = Field(default=None, ge=0)
    so2: float | None = Field(default=None, ge=0)
    co: float | None = Field(default=None, ge=0)
    data_quality: DataQuality
    is_simulated: bool = False


class ExposureContext(BaseModel):
    transportation: str = "MOSTLY_INDOORS"
    outdoor_duration_minutes: int = Field(default=30, ge=0)
    activity: str | None = None


class EnvironmentSummary(BaseModel):
    snapshot: EnvironmentSnapshot
    exposure_context: ExposureContext
