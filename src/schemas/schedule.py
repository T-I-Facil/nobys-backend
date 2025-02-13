from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Schedule(BaseModel):
    id: str
    user_id: str
    start_date: datetime
    schedule_time: int
    value: float
    invoiced: Optional[bool] = False
    specialty: Optional[str] = None
    description: Optional[str] = None