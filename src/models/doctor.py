from pydantic import BaseModel, field_validator
from typing import Optional
import bcrypt

class Doctor(BaseModel):
    username: str
    password: str
    email: Optional[str]
    crm: str
    is_admin: bool
    others: bool

    @field_validator("password")
    def hash_password(cls, value: str) -> str:
        salt = bcrypt.gensalt() 
        hashed = bcrypt.hashpw(value.encode('utf-8'), salt)
        return hashed.decode('utf-8') 
