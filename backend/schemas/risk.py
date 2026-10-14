from pydantic import BaseModel, Field


class RiskIndicator(BaseModel):
    name: str
    score: int = Field(ge=0, le=100)
    status: str
    explanation: str


class RiskSummary(BaseModel):
    overall_exposure: int = Field(ge=0, le=100)
    status: str
    indicators: list[RiskIndicator]
