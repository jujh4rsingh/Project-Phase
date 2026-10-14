from fastapi import APIRouter

from backend.schemas.location import LocationOption

router = APIRouter(prefix="/api/location", tags=["location"])

OPTIONS = [
    LocationOption(locality="Bengaluru", latitude=12.9716, longitude=77.5946, timezone="Asia/Kolkata"),
    LocationOption(locality="Mumbai", latitude=19.076, longitude=72.8777, timezone="Asia/Kolkata"),
    LocationOption(locality="Delhi", latitude=28.6139, longitude=77.209, timezone="Asia/Kolkata"),
    LocationOption(locality="Singapore", latitude=1.3521, longitude=103.8198, timezone="Asia/Singapore"),
    LocationOption(locality="London", latitude=51.5072, longitude=-0.1276, timezone="Europe/London"),
    LocationOption(locality="New York", latitude=40.7128, longitude=-74.006, timezone="America/New_York"),
]


@router.get("/options", response_model=list[LocationOption])
async def location_options() -> list[LocationOption]:
    return OPTIONS
