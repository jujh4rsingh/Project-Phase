from fastapi import APIRouter

from backend.schemas.dashboard import PlanItem
from backend.services.demo_store import store

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("", response_model=list[PlanItem])
async def recommendations() -> list[PlanItem]:
    return [PlanItem(title="Broad-spectrum sun protection", detail="Maintain your normal routine and follow your product directions during outdoor exposure.", reason="Current UV indicator is elevated."), PlanItem(title="Moisturizing focus", detail="Maintain your usual moisturizer while humidity is lower than your recent comfort range.", reason="Current profile and environment suggest dryness may be more noticeable.")]
