from fastapi import APIRouter

from backend.config import get_settings
from backend.schemas.environment import EnvironmentSnapshot, ExposureContext
from backend.services.environment_service import EnvironmentService
from backend.services.provider_factory import environment_provider

router = APIRouter(prefix="/api/environment", tags=["environment"])


@router.get("/current", response_model=EnvironmentSnapshot)
async def current_environment() -> EnvironmentSnapshot:
    settings = get_settings()
    weather, air, provider = environment_provider(settings)
    return await EnvironmentService(settings.demo_mode, weather, air, provider).current(ExposureContext())


@router.get("/forecast", response_model=list[EnvironmentSnapshot])
async def environment_forecast() -> list[EnvironmentSnapshot]:
    settings = get_settings()
    weather, air, provider = environment_provider(settings)
    snapshot = await EnvironmentService(settings.demo_mode, weather, air, provider).current(ExposureContext())
    return [snapshot]


@router.get("/history", response_model=list[EnvironmentSnapshot])
async def environment_history() -> list[EnvironmentSnapshot]:
    settings = get_settings()
    weather, air, provider = environment_provider(settings)
    snapshot = await EnvironmentService(settings.demo_mode, weather, air, provider).current(ExposureContext())
    return [snapshot]
