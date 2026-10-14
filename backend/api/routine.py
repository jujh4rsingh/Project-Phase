from fastapi import APIRouter

from backend.schemas.dashboard import PlanItem
from backend.services.demo_store import store

router = APIRouter(prefix="/api/routine", tags=["routine"])


@router.get("/today", response_model=list[PlanItem])
async def get_today_routine() -> list[PlanItem]:
    return [
        PlanItem(title="Morning routine", detail="Maintain your normal moisturizer and broad-spectrum sunscreen.", reason="Your profile and current UV conditions make sun protection relevant."),
        PlanItem(title="Outdoor commute", detail="Consider protective clothing, helmet, and visor during your motorcycle commute.", reason="Your transport context increases direct outdoor exposure."),
        PlanItem(title="Evening routine", detail="Consider gentle cleansing after prolonged outdoor exposure.", reason="This supports a stable routine after environmental exposure without prescribing treatment."),
    ]
