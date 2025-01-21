from pydantic import BaseModel
from typing import Optional

class Schedule(BaseModel):
    start_date: str
    end_date: str
    value: float
    specialty: Optional[str] = None
    description: Optional[str] = None