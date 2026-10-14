import asyncio
import json
import math
from datetime import UTC, datetime


class DeviceSimulator:
    """Generates gradual demo readings and never labels them as live measurements."""

    def __init__(self, device_id: str = "demo-device-001") -> None:
        self.device_id = device_id
        self.tick = 0

    def reading(self) -> dict[str, object]:
        self.tick += 1
        phase = self.tick / 8
        return {
            "device_id": self.device_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "temperature": round(27.4 + math.sin(phase) * 0.7, 1),
            "humidity": round(46.2 + math.cos(phase) * 1.5, 1),
            "pm25": round(31.5 + math.sin(phase / 2) * 2.2, 1),
            "pm10": round(48.2 + math.sin(phase / 2) * 3, 1),
            "co2": round(740 + math.sin(phase) * 20),
            "voc": round(120 + math.cos(phase) * 8),
            "uv": 0,
            "data_quality": "SIMULATED",
        }

    async def stream(self, interval_seconds: float = 5.0):
        while True:
            yield self.reading()
            await asyncio.sleep(interval_seconds)


if __name__ == "__main__":
    print(json.dumps(DeviceSimulator().reading(), indent=2))
