from fastapi import APIRouter

from backend.schemas.exposure import ExposureEvent, ExposureSummary
from backend.services.demo_store import store

router = APIRouter(prefix="/api/exposure", tags=["exposure"])


@router.get("/today", response_model=ExposureSummary)
async def get_today_exposure() -> ExposureSummary:
    return store.exposure_summary()


@router.get("/history", response_model=list[ExposureEvent])
async def get_exposure_history() -> list[ExposureEvent]:
    return store.exposure_events()
