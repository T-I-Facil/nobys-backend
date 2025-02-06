from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from mongo import UserRepository, SessionRepository
import bcrypt
from handlers import create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/v1")

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(credentials: LoginRequest):
    user_repo = UserRepository()
    user = user_repo.get_by_email(credentials.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stored_password = user["password"].encode('utf-8')
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), stored_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(user["_id"])})

    return JSONResponse(
        status_code=200,
        content={
            "message": "Login successful",
            "user": {
                "name": user["name"],
                "email": user.get("email", ""),
                "is_admin": user.get("is_admin", False),
                "user_id": str(user["_id"]),
            },
            "token": access_token
        },
    )

@router.post("/logout")
async def logout(token: str):
    session_repo = SessionRepository()
    session_repo.delete_session(token)

    return JSONResponse(
        status_code=200,
        content={"message": "Logout successful"},
    )

