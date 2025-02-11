from pydantic import BaseModel
from typing import Optional

class Hospital(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    website: Optional[str] = None

