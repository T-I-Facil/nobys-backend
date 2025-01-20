from pydantic import BaseModel
from typing import Optional

class Schedule(BaseModel):
    date: str
    time: str
    patient: str
    age: str
    value: float
    description: Optional[str] = None