from pathlib import Path

import yaml

from backend.schemas.environment import EnvironmentSnapshot, ExposureContext
from backend.schemas.risk import RiskIndicator, RiskSummary


class SkinRiskEngine:
    def __init__(self, rules_path: Path | None = None) -> None:
        path = rules_path or Path(__file__).parents[2] / "config" / "risk_rules.yaml"
        self.rules = yaml.safe_load(path.read_text(encoding="utf-8"))["risk_categories"]

    def calculate(
        self,
        environment: EnvironmentSnapshot,
        context: ExposureContext,
        skin_type: str = "Normal",
        sensitivity: str = "Moderate",
    ) -> RiskSummary:
        uv = self._uv_score(environment.uv_index or 0, context)
        pollution = self._pollution_score(environment.pm25 or 0, context, sensitivity)
        dryness = self._dryness_score(environment.humidity, environment.wind_speed or 0, skin_type)
        heat = self._heat_score(environment.temperature or 0, context)
        indicators = [uv, pollution, dryness, heat]
        overall = max(indicator.score for indicator in indicators)
        if sum(indicator.score for indicator in indicators) > 220:
            overall = min(100, overall + 10)
        status = "High" if overall >= 70 else "Elevated" if overall >= 45 else "Moderate" if overall >= 25 else "Low"
        return RiskSummary(overall_exposure=overall, status=status, indicators=indicators)

    def _uv_score(self, value: float, context: ExposureContext) -> RiskIndicator:
        score = min(100, round(value / 11 * 100))
        if context.outdoor_duration_minutes >= 60:
            score = min(100, score + 12)
        if context.transportation == "MOTORCYCLE":
            score = min(100, score + 8)
        return RiskIndicator(name="UV risk", score=score, status=self._status(score), explanation="UV is currently the dominant environmental exposure factor." if score >= 60 else "UV exposure is currently limited.")

    def _pollution_score(self, value: float, context: ExposureContext, sensitivity: str) -> RiskIndicator:
        score = min(100, round(value / 55 * 100))
        if context.outdoor_duration_minutes >= 60:
            score = min(100, score + 8)
        if sensitivity == "High":
            score = min(100, score + 10)
        return RiskIndicator(name="Pollution risk", score=score, status=self._status(score), explanation="Air pollution is elevated for the available outdoor data." if score >= 45 else "Air quality is currently good.")

    def _dryness_score(self, humidity: float | None, wind: float, skin_type: str) -> RiskIndicator:
        score = max(0, round((45 - (humidity or 45)) * 1.7)) + min(18, round(wind / 4))
        if skin_type == "Dry":
            score += 15
        score = min(100, score)
        return RiskIndicator(name="Dryness risk", score=score, status=self._status(score), explanation="Humidity is lower than the personal comfort range used by this indicator." if score >= 45 else "Humidity is not currently a strong dryness signal.")

    def _heat_score(self, temperature: float, context: ExposureContext) -> RiskIndicator:
        score = max(0, round((temperature - 22) * 5))
        if context.outdoor_duration_minutes >= 60:
            score += 8
        score = min(100, score)
        return RiskIndicator(name="Heat risk", score=score, status=self._status(score), explanation="Warm conditions and outdoor time may increase sweat and heat exposure." if score >= 45 else "Heat exposure is currently limited.")

    @staticmethod
    def _status(score: int) -> str:
        return "High" if score >= 70 else "Elevated" if score >= 45 else "Moderate" if score >= 25 else "Low"
