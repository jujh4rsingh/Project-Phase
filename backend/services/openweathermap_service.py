from typing import Any

import httpx


class OpenWeatherMapService:
    provider_name = "openweathermap"

    def __init__(self, api_key: str, weather_url: str, air_quality_url: str, timeout_seconds: float = 8.0) -> None:
        self.api_key = api_key
        self.weather_url = weather_url
        self.air_quality_url = air_quality_url
        self.timeout = httpx.Timeout(timeout_seconds)

    async def fetch_weather(self, latitude: float, longitude: float) -> dict[str, Any]:
        params = {"lat": latitude, "lon": longitude, "appid": self.api_key, "units": "metric"}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(self.weather_url, params=params)
            response.raise_for_status()
            payload = response.json()
        main = payload.get("main")
        wind = payload.get("wind", {})
        clouds = payload.get("clouds", {})
        if not isinstance(main, dict):
            raise ValueError("OpenWeatherMap response did not contain current conditions")
        return {"temperature": main.get("temp"), "humidity": main.get("humidity"), "apparent_temperature": main.get("feels_like"), "wind_speed": wind.get("speed"), "cloud_cover": clouds.get("all"), "precipitation": (payload.get("rain") or {}).get("1h", 0), "uv_index": None, "solar_radiation": None}

    async def fetch_air_quality(self, latitude: float, longitude: float) -> dict[str, Any]:
        params = {"lat": latitude, "lon": longitude, "appid": self.api_key}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(self.air_quality_url, params=params)
            response.raise_for_status()
            payload = response.json()
        item = (payload.get("list") or [{}])[0]
        components = item.get("components", {})
        if not isinstance(components, dict):
            raise ValueError("OpenWeatherMap air quality response did not contain components")
        aqi = (item.get("main") or {}).get("aqi")
        return {"pm25": components.get("pm2_5"), "pm10": components.get("pm10"), "ozone": components.get("o3"), "no2": components.get("no2"), "so2": components.get("so2"), "co": components.get("co"), "aqi": aqi * 20 if isinstance(aqi, (int, float)) else None}