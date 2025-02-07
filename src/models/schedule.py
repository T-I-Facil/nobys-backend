from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Schedule(BaseModel):
    start_date: datetime
    schedule_time: int
    value: float
    specialty: Optional[str] = None
    description: Optional[str] = None