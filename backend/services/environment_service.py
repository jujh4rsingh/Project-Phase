from datetime import UTC, datetime
import math
import httpx

from backend.schemas.environment import DataQuality, EnvironmentSnapshot, ExposureContext
from backend.services.air_quality_service import AirQualityService
from backend.services.weather_service import WeatherService


class EnvironmentService:
    """Provides a stable environment contract while external providers are unavailable."""

    def __init__(self, demo_mode: bool = True, weather_service: WeatherService | None = None, air_quality_service: AirQualityService | None = None, provider: object | None = None) -> None:
        self.demo_mode = demo_mode
        self.weather_service = weather_service
        self.air_quality_service = air_quality_service
        self.provider = provider

    async def current(self, context: ExposureContext | None = None, latitude: float = 12.9716, longitude: float = 77.5946) -> EnvironmentSnapshot:
        if not self.demo_mode and self.provider:
            try:
                weather, air = await self._fetch_provider(latitude, longitude)
                return self._live_snapshot(weather, air)
            except (RuntimeError, ValueError, KeyError, httpx.HTTPError):
                return self._simulated_snapshot(latitude, longitude, DataQuality.UNAVAILABLE)
        if not self.demo_mode and self.weather_service and self.air_quality_service:
            try:
                weather, air = await self._fetch_live(latitude, longitude)
                return self._live_snapshot(weather, air, "open-meteo")
            except (RuntimeError, ValueError, KeyError, httpx.HTTPError):
                return self._simulated_snapshot(latitude, longitude, DataQuality.UNAVAILABLE)
        return self._simulated_snapshot(latitude, longitude, DataQuality.SIMULATED)

    async def _fetch_live(self, latitude: float, longitude: float) -> tuple[dict, dict]:
        import asyncio
        weather, air = await asyncio.gather(self.weather_service.fetch(latitude, longitude), self.air_quality_service.fetch(latitude, longitude))
        return weather, air

    async def _fetch_provider(self, latitude: float, longitude: float) -> tuple[dict, dict]:
        import asyncio
        weather, air = await asyncio.gather(self.provider.fetch_weather(latitude, longitude), self.provider.fetch_air_quality(latitude, longitude))
        return weather, air

    def _live_snapshot(self, weather: dict, air: dict, source: str = "openweathermap") -> EnvironmentSnapshot:
        return EnvironmentSnapshot(
            timestamp=datetime.now(UTC), source=source, temperature=weather.get("temperature", weather.get("temperature_2m")),
            humidity=weather.get("humidity", weather.get("relative_humidity_2m")), apparent_temperature=weather.get("apparent_temperature", weather.get("feels_like")),
            uv_index=weather.get("uv_index"), solar_radiation=weather.get("solar_radiation", weather.get("shortwave_radiation")),
            precipitation=weather.get("precipitation"), cloud_cover=weather.get("cloud_cover"), wind_speed=weather.get("wind_speed", weather.get("wind_speed_10m")),
            pm25=air.get("pm25", air.get("pm2_5")), pm10=air.get("pm10"), ozone=air.get("ozone"), no2=air.get("no2", air.get("nitrogen_dioxide")),
            so2=air.get("so2", air.get("sulphur_dioxide")), co=air.get("co", air.get("carbon_monoxide")), aqi=air.get("aqi", air.get("us_aqi")),
            data_quality=DataQuality.LIVE,
        )

    def _simulated_snapshot(self, latitude: float, longitude: float, quality: DataQuality) -> EnvironmentSnapshot:
        location_factor = round(abs(latitude - 12.9716) / 20, 2)
        phase = datetime.now(UTC).timestamp() / 90
        variation = math.sin(phase) * 0.7
        return EnvironmentSnapshot(
            timestamp=datetime.now(UTC),
            source="simulated-outdoor-fallback" if quality == DataQuality.UNAVAILABLE else "demo-outdoor-simulator",
            temperature=round(29.0 + location_factor * 8 + variation, 1),
            humidity=round(max(22, 31.0 - location_factor * 12 - variation), 1),
            apparent_temperature=round(31.0 + variation, 1),
            uv_index=round(min(11, 7.2 + location_factor * 1.4 + variation / 3), 1),
            pm25=round(max(2, 12.0 + variation * 2), 1),
            pm10=22.0,
            aqi=42.0,
            wind_speed=14.0,
            cloud_cover=19.0,
            data_quality=quality,
            is_simulated=quality != DataQuality.LIVE,
        )
