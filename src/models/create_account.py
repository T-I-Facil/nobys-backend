from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    name: str
    last_name: str
    password: str
    email: EmailStr
    cpf: str