from fastapi import APIRouter, HTTPException

from backend.schemas.alert import Alert
from backend.services.demo_store import store

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=list[Alert])
async def get_alerts() -> list[Alert]:
    return store.active_alerts()


@router.post("/{alert_id}/acknowledge", response_model=Alert)
async def acknowledge_alert(alert_id: str) -> Alert:
    alert = store.acknowledge(alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert
