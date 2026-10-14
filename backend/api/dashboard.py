from fastapi import APIRouter, Query

from backend.config import get_settings
from backend.schemas.dashboard import DashboardResponse
from backend.schemas.environment import ExposureContext
from backend.services.adaptive_skincare import AdaptiveSkincareEngine
from backend.services.environment_service import EnvironmentService
from backend.services.provider_factory import environment_provider
from backend.services.risk_engine import SkinRiskEngine

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
async def get_dashboard(latitude: float = Query(12.9716, ge=-90, le=90), longitude: float = Query(77.5946, ge=-180, le=180)) -> DashboardResponse:
    settings = get_settings()
    context = ExposureContext(transportation="MOTORCYCLE", outdoor_duration_minutes=90)
    weather, air, provider = environment_provider(settings)
    environment = await EnvironmentService(settings.demo_mode, weather, air, provider).current(context, latitude, longitude)
    risk = SkinRiskEngine().calculate(environment, context, skin_type="Dry", sensitivity="Moderate")
    plan = AdaptiveSkincareEngine().build_plan(environment, context, risk)
    return DashboardResponse(environment=environment, exposure_context=context, risk=risk, plan=plan, demo_mode=settings.demo_mode)
