# Atmo Derma

Atmo Derma is an environmental skin intelligence platform that connects outdoor conditions, indoor sensor data, exposure context, and personal skin observations into explainable wellness guidance.

## Current project state

The repository started empty. The current MVP includes a FastAPI backend, React + TypeScript + Vite frontend, environment-based configuration, profile/check-in/exposure/alert workflows, explainable risk and routine guidance, a simulated indoor device, and a PostgreSQL/Alembic persistence boundary.

## Architecture

- `backend/`: FastAPI API, services, risk and exposure engines, persistence adapters, and IoT integrations.
- `frontend/`: React + TypeScript client for dashboard, onboarding, environment, skin, routine, exposure, insights, devices, profile, and settings views.
- `config/`: versioned, explainable risk rules and non-secret configuration.
- `docs/`: architecture, API, privacy, and development notes.

## Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 15+ for persistence (demo startup currently does not require a database)
- Optional MQTT broker for physical or simulated device integration

## Phase 1 startup

```powershell
cd "D:\PP Project"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
uvicorn backend.main:app --reload
```

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

The API health check is available at `http://localhost:8000/health`; the frontend runs at `http://localhost:5173`.

## Configuration

Copy `.env.example` to `.env`. Credentials and secrets stay outside source control. Outdoor data uses Open-Meteo live services by default; set `DEMO_MODE=true` only when you want synthetic outdoor fallback values. Indoor device readings remain explicitly simulated until hardware is connected.

## Product safety

Atmo Derma provides environmental and self-reported wellness indicators, not medical diagnoses or treatment. Recommendations use cautious, explainable language and are based on available data.
