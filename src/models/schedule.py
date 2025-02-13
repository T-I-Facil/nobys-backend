from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateScheduleRequest(BaseModel):
    start_date: datetime
    schedule_time: int
    value: float
    specialty: Optional[str] = None
    description: Optional[str] = None

class GetSchedulesResponse(BaseModel):
    id: str
    user_id: str
    start_date: datetime
    schedule_time: int
    value: float
    invoiced: Optional[bool] = False
    specialty: Optional[str] = None
    description: Optional[str] = None