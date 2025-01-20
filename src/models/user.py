from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional
import bcrypt

class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    crm: Optional[str] = None
    is_admin: Optional[bool] = False
    is_confirmed: Optional[bool] = False
    others: Optional[bool] = False

    @field_validator("password")
    def hash_password(cls, value: str) -> str:
        salt = bcrypt.gensalt() 
        hashed = bcrypt.hashpw(value.encode('utf-8'), salt)
        return hashed.decode('utf-8') 
