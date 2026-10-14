from backend.schemas.environment import DataQuality, EnvironmentSnapshot, ExposureContext
from backend.services.risk_engine import SkinRiskEngine


def test_dry_profile_and_low_humidity_raise_dryness_indicator() -> None:
    environment = EnvironmentSnapshot(
        timestamp="2026-09-16T08:00:00Z", source="test", humidity=25, temperature=27,
        wind_speed=12, data_quality=DataQuality.LIVE,
    )

    result = SkinRiskEngine().calculate(environment, ExposureContext(), skin_type="Dry")
    dryness = next(item for item in result.indicators if item.name == "Dryness risk")

    assert dryness.score >= 45
    assert "Humidity" in dryness.explanation


def test_motorcycle_context_increases_uv_indicator() -> None:
    environment = EnvironmentSnapshot(
        timestamp="2026-09-16T08:00:00Z", source="test", uv_index=7,
        data_quality=DataQuality.LIVE,
    )

    walking = SkinRiskEngine().calculate(environment, ExposureContext(transportation="WALKING"))
    motorcycle = SkinRiskEngine().calculate(environment, ExposureContext(transportation="MOTORCYCLE"))

    walking_uv = next(item for item in walking.indicators if item.name == "UV risk")
    motorcycle_uv = next(item for item in motorcycle.indicators if item.name == "UV risk")
    assert motorcycle_uv.score > walking_uv.score
