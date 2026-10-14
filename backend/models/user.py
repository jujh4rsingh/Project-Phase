from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.database import Base


class UserRecord(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    display_name: Mapped[str] = mapped_column(String(120))
    age: Mapped[int] = mapped_column()
    skin_type: Mapped[str] = mapped_column(String(30), default="Unsure")
    sensitivity: Mapped[str] = mapped_column(String(30), default="Unsure")
    concerns: Mapped[list[str]] = mapped_column(JSON, default=list)
    transportation: Mapped[str] = mapped_column(String(40), default="MOSTLY_INDOORS")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
