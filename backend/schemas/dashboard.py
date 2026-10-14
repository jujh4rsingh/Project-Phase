from pydantic import BaseModel

from backend.schemas.environment import EnvironmentSnapshot, ExposureContext
from backend.schemas.risk import RiskSummary


class PlanItem(BaseModel):
    title: str
    detail: str
    reason: str


class DashboardResponse(BaseModel):
    environment: EnvironmentSnapshot
    exposure_context: ExposureContext
    risk: RiskSummary
    plan: list[PlanItem]
    demo_mode: bool
