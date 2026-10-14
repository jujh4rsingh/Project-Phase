from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    age: int = Field(ge=13, le=120)
    skin_type: str = "Unsure"
    sensitivity: str = "Unsure"
    concerns: list[str] = []
    transportation: str = "MOSTLY_INDOORS"
    outdoor_exposure: str = "LESS_THAN_30_MINUTES"
    sunscreen_usage: str = "UNSURE"
    location_enabled: bool = False


class UserCreate(UserProfile):
    display_name: str = "Alex"


class UserResponse(UserCreate):
    id: str
