from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.alerts import router as alerts_router
from backend.api.combined import router as combined_router
from backend.api.dashboard import router as dashboard_router
from backend.api.devices import router as devices_router
from backend.api.environment import router as environment_router
from backend.api.exposure import router as exposure_router
from backend.api.insights import router as insights_router
from backend.api.indoor import router as indoor_router
from backend.api.location import router as location_router
from backend.api.photo import router as photo_router
from backend.api.recommendations import router as recommendations_router
from backend.api.reasoning import router as reasoning_router
from backend.api.risk import router as risk_router
from backend.api.routine import router as routine_router
from backend.api.skin import router as skin_router
from backend.api.users import router as users_router
from backend.config import get_settings

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Environmental skin intelligence API.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(dashboard_router)
app.include_router(environment_router)
app.include_router(risk_router)
app.include_router(users_router)
app.include_router(skin_router)
app.include_router(exposure_router)
app.include_router(alerts_router)
app.include_router(combined_router)
app.include_router(routine_router)
app.include_router(recommendations_router)
app.include_router(insights_router)
app.include_router(devices_router)
app.include_router(location_router)
app.include_router(indoor_router)
app.include_router(reasoning_router)
app.include_router(photo_router)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str | bool]:
    return {"status": "ok", "service": settings.app_name, "demo_mode": settings.demo_mode}
