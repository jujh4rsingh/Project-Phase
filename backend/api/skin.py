from fastapi import APIRouter

from backend.schemas.skin import SkinCheckinCreate, SkinState, SkinTrend
from backend.services.demo_store import store

router = APIRouter(prefix="/api/users/{user_id}", tags=["skin"])


@router.post("/checkin", response_model=SkinState)
async def create_checkin(user_id: str, payload: SkinCheckinCreate) -> SkinState:
    return store.add_checkin(payload)


@router.get("/skin-state", response_model=SkinState | None)
async def get_skin_state(user_id: str) -> SkinState | None:
    return store.checkins[-1] if store.checkins else None


@router.get("/skin-trends", response_model=SkinTrend)
async def get_skin_trends(user_id: str) -> SkinTrend:
    return store.trend()
