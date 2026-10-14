from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Atmo Derma"
    database_url: str = "postgresql+asyncpg://atmo_derma:change-me@localhost:5432/atmo_derma"
    openmeteo_base_url: str = "https://api.open-meteo.com/v1/forecast"
    openmeteo_air_quality_url: str = "https://air-quality-api.open-meteo.com/v1/air-quality"
    openweathermap_api_key: str | None = None
    openweathermap_base_url: str = "https://api.openweathermap.org/data/2.5/weather"
    openweathermap_air_quality_url: str = "https://api.openweathermap.org/data/2.5/air_pollution"
    mqtt_broker: str = "localhost"
    mqtt_port: int = 1883
    mqtt_username: str | None = None
    mqtt_password: str | None = None
    secret_key: str = "development-only-change-me"
    demo_mode: bool = False
    environment_refresh_minutes: int = 10
    environment_poll_seconds: int = 15
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
