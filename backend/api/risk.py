from fastapi import APIRouter

from backend.config import get_settings
from backend.schemas.environment import ExposureContext
from backend.schemas.risk import RiskSummary
from backend.services.environment_service import EnvironmentService
from backend.services.risk_engine import SkinRiskEngine

router = APIRouter(prefix="/api/risk", tags=["risk"])


@router.get("/current", response_model=RiskSummary)
async def current_risk() -> RiskSummary:
    context = ExposureContext(transportation="MOTORCYCLE", outdoor_duration_minutes=90)
    environment = await EnvironmentService(get_settings().demo_mode).current(context)
    return SkinRiskEngine().calculate(environment, context, skin_type="Dry", sensitivity="Moderate")


@router.get("/history", response_model=list[RiskSummary])
async def risk_history() -> list[RiskSummary]:
    return [await current_risk()]
