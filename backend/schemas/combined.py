from pydantic import BaseModel

from backend.schemas.environment import EnvironmentSnapshot
from backend.schemas.photo import PhotoAnalysisResult
from backend.schemas.risk import RiskSummary


class CombinedSkinInsight(BaseModel):
    photo: PhotoAnalysisResult
    environment: EnvironmentSnapshot
    risk: RiskSummary
    profile_context: str
    insight: str
    data_sources: list[str]