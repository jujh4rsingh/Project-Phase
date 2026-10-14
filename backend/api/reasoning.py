from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/reasoning", tags=["reasoning"])


class ReasoningResponse(BaseModel):
    title: str
    summary: str
    factors: list[str]
    safety_note: str


@router.get("/dashboard", response_model=ReasoningResponse)
async def dashboard_reasoning() -> ReasoningResponse:
    return ReasoningResponse(title="Why is exposure elevated?", summary="The indicator is driven by current UV, outdoor duration, and motorcycle commute context. Humidity is also below the demo profile's recent baseline.", factors=["UV index: 7.2", "Outdoor context: 90 minutes", "Transport: motorcycle", "Humidity: 31% vs recent reference of 47%"], safety_note="This is a relative environmental indicator, not a clinical or diagnostic score.")
