from backend.schemas.dashboard import PlanItem
from backend.schemas.environment import EnvironmentSnapshot, ExposureContext
from backend.schemas.risk import RiskSummary


class AdaptiveSkincareEngine:
    def build_plan(self, environment: EnvironmentSnapshot, context: ExposureContext, risk: RiskSummary) -> list[PlanItem]:
        plan = [PlanItem(title="Maintain your normal morning routine", detail="Moisturizer and your usual broad-spectrum sunscreen.", reason="Your routine remains the most stable starting point for today's conditions.")]
        if next((item for item in risk.indicators if item.name == "UV risk"), None).score >= 45:
            detail = "Consider protective clothing and reduce prolonged direct exposure where practical."
            if context.transportation == "MOTORCYCLE":
                detail = "Consider sunscreen plus appropriate helmet, visor, and protective clothing for the outdoor commute."
            plan.append(PlanItem(title="Before outdoor exposure", detail=detail, reason="UV and outdoor exposure context are elevated."))
        if (environment.pm25 or 0) >= 25:
            plan.append(PlanItem(title="After prolonged outdoor exposure", detail="Consider gentle cleansing without unnecessary aggressive scrubbing.", reason="Available PM2.5 data is elevated."))
        if (environment.humidity or 45) < 35:
            plan.append(PlanItem(title="Keep moisturizing in focus", detail="Maintain your usual moisturizer and avoid unnecessarily harsh cleansing.", reason="Humidity is lower than the recent comfort range used by this demo profile."))
        return plan
