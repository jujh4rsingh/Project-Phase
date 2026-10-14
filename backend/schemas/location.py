from pydantic import BaseModel, Field


class LocationContext(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    locality: str
    timezone: str = "auto"
    source: str = "MANUAL"


class LocationOption(BaseModel):
    locality: str
    latitude: float
    longitude: float
    timezone: str
