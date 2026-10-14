from typing import Any

import httpx


class AirQualityService:
    def __init__(self, base_url: str, timeout_seconds: float = 8.0) -> None:
        self.base_url = base_url
        self.timeout = httpx.Timeout(timeout_seconds)

    async def fetch(self, latitude: float, longitude: float) -> dict[str, Any]:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi,european_aqi",
            "timezone": "auto",
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            payload = response.json()
        current = payload.get("current")
        if not isinstance(current, dict):
            raise ValueError("Open-Meteo air quality response did not contain current conditions")
        return current
