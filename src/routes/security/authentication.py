from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from mongo import UserRepository
import bcrypt
from pydantic import BaseModel

router = APIRouter(prefix="/v1")

class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(credentials: LoginRequest):
    user_repo = UserRepository()
    user = user_repo.get_by_username(credentials.username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stored_password = user["password"].encode('utf-8')
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), stored_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return JSONResponse(
        status_code=200,
        content={
            "message": "Login successful",
            "user": {
                "username": user["username"],
                "email": user.get("email", ""),
                "is_admin": user.get("is_admin", False),
            },
        },
    )

