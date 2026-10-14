from datetime import UTC, datetime

from fastapi import APIRouter

from backend.iot.device_simulator import DeviceSimulator
from backend.schemas.indoor import IndoorDemoSettings, IndoorEnvironment

router = APIRouter(prefix="/api/indoor", tags=["indoor"])
simulator = DeviceSimulator()
settings = IndoorDemoSettings(temperature=27.4, humidity=46.2, pm25=31.5, co2=740, voc=120)


def current() -> IndoorEnvironment:
    value = simulator.reading()
    return IndoorEnvironment(temperature=float(value["temperature"]), humidity=float(value["humidity"]), pm25=float(value["pm25"]), pm10=float(value["pm10"]), co2=float(value["co2"]), voc=float(value["voc"]), data_quality="SIMULATED", updated_at=datetime.now(UTC).isoformat())


@router.get("/current", response_model=IndoorEnvironment)
async def current_indoor() -> IndoorEnvironment:
    return current()


@router.put("/demo", response_model=IndoorEnvironment)
async def update_demo(payload: IndoorDemoSettings) -> IndoorEnvironment:
    global settings
    settings = payload
    return IndoorEnvironment(temperature=payload.temperature, humidity=payload.humidity, pm25=payload.pm25, pm10=payload.pm25 * 1.45, co2=payload.co2, voc=payload.voc, data_quality="SIMULATED", updated_at=datetime.now(UTC).isoformat())
