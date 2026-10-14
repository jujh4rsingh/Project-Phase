# Development

## Backend

```powershell
cd "D:\PP Project"
python -m pip install -r backend\requirements.txt
python -m pytest backend\tests -q
uvicorn backend.main:app --reload
```

## Frontend

```powershell
cd frontend
npm install
npm run build
npm run dev
```

## Demo IoT reading

```powershell
python -m backend.iot.device_simulator
```

The current MVP uses `DEMO_MODE=true` by default. Demo outdoor values evolve over refreshes and are labeled `SIMULATED`. To use live Open-Meteo weather and air quality, set `DEMO_MODE=false`; the provider services apply timeout/error handling and return `UNAVAILABLE` simulated fallback data if the external service cannot be reached. The dashboard polls every 15 seconds in the browser, while indoor simulator readings are available near real-time.

To use OpenWeatherMap instead, set `OPENWEATHERMAP_API_KEY` in `.env`. When that key is present, Atmo Derma uses the OpenWeatherMap current weather and air pollution endpoints. Never commit the key or paste it into source files.

Photo analysis is intentionally not a medical or face-diagnosis model. It validates the uploaded image, measures dimensions, brightness, contrast, and conservative pixel-derived visual indicators, then discards the original bytes. A future computer-vision model can replace this service without changing the API contract.
