# API

The API is served by FastAPI at `http://localhost:8000`.

- `GET /health` returns service and demo-mode status.
- `GET /api/dashboard` composes the current environment, exposure context, risk indicators, and adaptive plan.
- `GET /api/environment/current`, `/forecast`, and `/history` expose normalized environment snapshots.
- `GET /api/risk/current` and `/history` expose explainable environmental indicators.
- `POST /api/users` and `PUT /api/users/{user_id}/profile` support profile setup.
- `POST /api/users/{user_id}/checkin` records a lightweight daily skin observation.
- `GET /api/users/{user_id}/skin-state` and `/skin-trends` expose recent state and personal trend status.
- `GET /api/exposure/today` and `/history` expose demo exposure history.
- `GET /api/alerts` and `POST /api/alerts/{alert_id}/acknowledge` support contextual alerts.
- `GET /api/routine/today` and `GET /api/recommendations` expose explainable guidance.
- `GET /api/devices` and `/api/devices/{device_id}/readings` expose the simulated indoor sensor.
- `GET /api/insights/daily` and `/weekly` expose traceable insights.
- `POST /api/users/{user_id}/skin-insight` combines an uploaded image with profile, location, live environment, and exposure risk.
- `GET /docs` provides the generated OpenAPI explorer.

The dashboard and demo workflow currently use a clearly labeled simulated environment when `DEMO_MODE=true`. Provider integrations are isolated in `WeatherService` and `AirQualityService`. The demo store is intentionally replaceable by the async SQLAlchemy/Alembic persistence boundary in `backend/database`, `backend/models`, and `backend/migrations`.

`GET /api/dashboard` accepts `latitude` and `longitude` query parameters. In live mode it calls Open-Meteo; in demo mode it returns changing synthetic values. `POST /api/users/{user_id}/skin-photo/analyze` accepts a multipart image and returns quality plus pixel-derived visual indicators, never a medical conclusion.

## Free data providers

- **Open-Meteo Weather API**: free and keyless for normal non-commercial use. Provides temperature, humidity, apparent temperature, wind, UV, cloud cover, precipitation, and solar radiation.
- **Open-Meteo Air Quality API**: free and keyless for normal non-commercial use. Provides PM2.5, PM10, ozone, NO2, CO, SO2, and AQI values.
- **Image analysis**: Atmo Derma currently uses local Pillow-based validation and pixel-derived visual indicators, so the original image does not leave the application. There is no dependable universal free dermatology diagnosis API; future computer-vision providers should remain optional and non-diagnostic.
