from datetime import UTC, datetime, timedelta
from uuid import uuid4

from backend.schemas.alert import Alert
from backend.schemas.exposure import ExposureEvent, ExposureSummary
from backend.schemas.skin import SkinCheckinCreate, SkinState, SkinTrend
from backend.schemas.user import UserCreate, UserResponse


class DemoStore:
    def __init__(self) -> None:
        self.user = UserResponse(id="demo-user-001", **UserCreate(age=29, display_name="Alex Shah", skin_type="Dry", sensitivity="Moderate", transportation="MOTORCYCLE", outdoor_exposure="ONE_TO_THREE_HOURS").model_dump())
        self.checkins: list[SkinState] = []
        now = datetime.now(UTC)
        self.alerts = [Alert(id="alert-uv", type="HIGH_UV", severity="elevated", title="UV exposure is currently elevated", message="UV is the dominant environmental exposure factor right now.", recommendation="Consider your normal broad-spectrum sun protection routine and reduce prolonged direct exposure where practical.", timestamp=now, source="risk-engine")]

    def create_user(self, payload: UserCreate) -> UserResponse:
        self.user = UserResponse(id=self.user.id, **payload.model_dump())
        return self.user

    def add_checkin(self, payload: SkinCheckinCreate) -> SkinState:
        state = SkinState(
            timestamp=datetime.now(UTC),
            dryness_indicator=75 if payload.feeling in {"Dry", "Tight"} or payload.appearance == "More dry than usual" else 35,
            oiliness_indicator=70 if payload.feeling == "Oily" or payload.appearance == "More oily than usual" else 30,
            redness_indicator=70 if payload.appearance == "Red" else 25,
            user_reported_irritation=payload.irritation,
            notes=payload.note,
        )
        self.checkins.append(state)
        return state

    def trend(self) -> SkinTrend:
        count = len(self.checkins)
        if count < 2:
            return SkinTrend(trend="INSUFFICIENT_DATA", explanation="Atmo Derma needs more than one observation before describing a personal trend.", observation_count=count)
        recent = sum(item.dryness_indicator for item in self.checkins[-3:]) / min(3, count)
        return SkinTrend(trend="CHANGING" if recent >= 55 else "STABLE", explanation="Recent dryness reports are being compared with your personal observations, not a population average.", observation_count=count)

    def exposure_summary(self) -> ExposureSummary:
        return ExposureSummary(date=datetime.now(UTC).date().isoformat(), outdoor_minutes=252, high_uv_minutes=68, elevated_pollution_minutes=0, highest_exposure_period="12:30 PM - 2:00 PM", transport_context=self.user.transportation, indoor_air_quality="Good", source="demo-exposure-estimate")

    def exposure_events(self) -> list[ExposureEvent]:
        now = datetime.now(UTC)
        return [ExposureEvent(timestamp=now - timedelta(hours=2), duration_minutes=90, context=self.user.transportation, uv_status="HIGH", pollution_status="GOOD"), ExposureEvent(timestamp=now - timedelta(hours=6), duration_minutes=42, context="INDOOR", uv_status="LOW", pollution_status="GOOD")]

    def active_alerts(self) -> list[Alert]:
        return [alert for alert in self.alerts if not alert.acknowledged]

    def acknowledge(self, alert_id: str) -> Alert | None:
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                return alert
        return None


store = DemoStore()
