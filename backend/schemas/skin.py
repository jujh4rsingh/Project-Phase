from datetime import datetime

from pydantic import BaseModel, Field


class SkinCheckinCreate(BaseModel):
    feeling: str
    appearance: str
    irritation: str
    outdoor_exposure: str
    sunscreen: str
    routine: str
    note: str | None = Field(default=None, max_length=500)


class SkinState(BaseModel):
    timestamp: datetime
    dryness_indicator: int = Field(ge=0, le=100)
    oiliness_indicator: int = Field(ge=0, le=100)
    redness_indicator: int = Field(ge=0, le=100)
    user_reported_irritation: str
    source: str = "DAILY_CHECKIN"
    notes: str | None = None


class SkinTrend(BaseModel):
    trend: str
    explanation: str
    observation_count: int
