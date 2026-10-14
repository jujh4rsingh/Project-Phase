from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.database import Base


class SkinCheckinRecord(Base):
    __tablename__ = "checkins"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    feeling: Mapped[str] = mapped_column(String(30))
    appearance: Mapped[str] = mapped_column(String(50))
    irritation: Mapped[str] = mapped_column(String(30))
    note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class SkinStateRecord(Base):
    __tablename__ = "skin_states"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    dryness_indicator: Mapped[int] = mapped_column(Integer)
    oiliness_indicator: Mapped[int] = mapped_column(Integer)
    redness_indicator: Mapped[int] = mapped_column(Integer)
    irritation: Mapped[str] = mapped_column(String(30))
    source: Mapped[str] = mapped_column(String(30), default="DAILY_CHECKIN")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
