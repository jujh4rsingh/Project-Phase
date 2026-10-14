from pydantic import BaseModel, Field


class PhotoAnalysisResult(BaseModel):
    image_quality: int = Field(ge=0, le=100)
    lighting_quality: int = Field(ge=0, le=100)
    face_visibility: int = Field(ge=0, le=100)
    analysis_possible: bool
    message: str
    dryness_indicator: int | None = Field(default=None, ge=0, le=100)
    redness_indicator: int | None = Field(default=None, ge=0, le=100)
    visible_blemish_indicator: int | None = Field(default=None, ge=0, le=100)
    confidence: int | None = Field(default=None, ge=0, le=100)
    source: str = "RULE_BASED_PLACEHOLDER"
