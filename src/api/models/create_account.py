from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    last_name: str
    password: str
    email: EmailStr
    cpf: str