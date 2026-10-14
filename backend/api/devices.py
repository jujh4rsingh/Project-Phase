from datetime import UTC, datetime

from fastapi import APIRouter

from backend.iot.device_simulator import DeviceSimulator
from backend.schemas.device import DeviceStatus, SensorReading

router = APIRouter(prefix="/api/devices", tags=["devices"])
simulator = DeviceSimulator()


@router.get("", response_model=list[DeviceStatus])
async def devices() -> list[DeviceStatus]:
    return [DeviceStatus(device_id=simulator.device_id, name="Demo indoor sensor", connected=True, last_seen=datetime.now(UTC), data_quality="SIMULATED", sensors=["temperature", "humidity", "PM2.5", "PM10", "CO2-equivalent", "VOC"])]


@router.get("/{device_id}", response_model=DeviceStatus)
async def device(device_id: str) -> DeviceStatus:
    return (await devices())[0]


@router.get("/{device_id}/readings", response_model=list[SensorReading])
async def readings(device_id: str) -> list[SensorReading]:
    value = simulator.reading()
    return [SensorReading(timestamp=datetime.fromisoformat(str(value["timestamp"])), temperature=float(value["temperature"]), humidity=float(value["humidity"]), pm25=float(value["pm25"]), pm10=float(value["pm10"]), co2=float(value["co2"]), voc=float(value["voc"]), uv=float(value["uv"]), data_quality="SIMULATED")]
