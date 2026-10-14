from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from backend.config import get_settings
from backend.schemas.combined import CombinedSkinInsight
from backend.schemas.environment import ExposureContext
from backend.schemas.photo import PhotoAnalysisResult
from backend.services.environment_service import EnvironmentService
from backend.services.provider_factory import environment_provider
from backend.services.risk_engine import SkinRiskEngine
from backend.services.skin_analysis import analyze_image
from backend.services.weather_service import WeatherService

router = APIRouter(prefix="/api/users/{user_id}", tags=["combined-analysis"])
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 8 * 1024 * 1024


@router.post("/skin-insight", response_model=CombinedSkinInsight)
async def combined_skin_insight(
    user_id: str,
    photo: UploadFile = File(...),
    latitude: float = Query(12.9716, ge=-90, le=90),
    longitude: float = Query(77.5946, ge=-180, le=180),
    skin_type: str = Query("Dry"),
    sensitivity: str = Query("Moderate"),
    transportation: str = Query("MOTORCYCLE"),
) -> CombinedSkinInsight:
    if photo.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Use a JPEG, PNG, or WebP image.")
    content = await photo.read(MAX_BYTES + 1)
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 8 MB or smaller.")
    photo_result = analyze_image(content)
    settings = get_settings()
    context = ExposureContext(transportation=transportation, outdoor_duration_minutes=90)
    weather, air, provider = environment_provider(settings)
    environment = await EnvironmentService(settings.demo_mode, weather, air, provider).current(context, latitude, longitude)
    risk = SkinRiskEngine().calculate(environment, context, skin_type=skin_type, sensitivity=sensitivity)
    insight = "The uploaded image could not be compared with environmental context." if not photo_result.analysis_possible else f"Your visual dryness indicator is {photo_result.dryness_indicator}/100 while current humidity is {environment.humidity}%. These observations occurred together and may help track your personal pattern over time."
    return CombinedSkinInsight(photo=photo_result, environment=environment, risk=risk, profile_context=f"{skin_type} skin profile, {sensitivity} sensitivity, {transportation.lower()} context", insight=insight, data_sources=[photo_result.source, environment.source, environment.data_quality.value])