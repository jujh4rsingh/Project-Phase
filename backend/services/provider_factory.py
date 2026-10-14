from backend.config import Settings
from backend.services.air_quality_service import AirQualityService
from backend.services.openweathermap_service import OpenWeatherMapService
from backend.services.weather_service import WeatherService


def environment_provider(settings: Settings) -> tuple[object | None, object | None, object | None]:
    if settings.openweathermap_api_key:
        provider = OpenWeatherMapService(settings.openweathermap_api_key, settings.openweathermap_base_url, settings.openweathermap_air_quality_url)
        return provider, None, provider
    return WeatherService(settings.openmeteo_base_url), AirQualityService(settings.openmeteo_air_quality_url), None
