from pydantic import BaseModel
from typing import Optional

class CreateHospital(BaseModel):
    name: str
    address: str
    phone: str
    email: str

