from datetime import datetime

from pydantic import BaseModel


class Alert(BaseModel):
    id: str
    type: str
    severity: str
    title: str
    message: str
    recommendation: str
    timestamp: datetime
    source: str
    acknowledged: bool = False
