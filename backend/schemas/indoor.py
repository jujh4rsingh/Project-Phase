from pydantic import BaseModel, Field


class IndoorDemoSettings(BaseModel):
    temperature: float = Field(ge=-20, le=60)
    humidity: float = Field(ge=0, le=100)
    pm25: float = Field(ge=0, le=500)
    co2: float = Field(ge=0, le=10000)
    voc: float = Field(ge=0, le=5000)


class IndoorEnvironment(BaseModel):
    temperature: float
    humidity: float
    pm25: float
    pm10: float
    co2: float
    voc: float
    data_quality: str
    updated_at: str
