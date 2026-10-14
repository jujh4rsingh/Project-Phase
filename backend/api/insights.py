from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.demo_store import store

router = APIRouter(prefix="/api/insights", tags=["insights"])


class Insight(BaseModel):
    title: str
    message: str
    source: str


@router.get("/daily", response_model=list[Insight])
async def daily_insights() -> list[Insight]:
    return [Insight(title="UV is dominant today", message="UV exposure is currently the largest environmental factor in your indicator.", source="risk-engine"), Insight(title="Dryness is worth watching", message="Humidity is lower than the comfort range used by your current profile.", source="environment-and-profile")]


@router.get("/weekly", response_model=list[Insight])
async def weekly_insights() -> list[Insight]:
    return [Insight(title="Build your personal baseline", message=f"Atmo Derma has {len(store.checkins)} recent check-in observations so far. Trends become more useful as your own history grows.", source="skin-trend-engine")]
