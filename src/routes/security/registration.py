from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from itsdangerous import URLSafeTimedSerializer
from models.user import User
from mongo import UserRepository
from handlers import send_confirmation_email

router = APIRouter(prefix="/v1")
serializer = URLSafeTimedSerializer("secret-key")

@router.post("/register")
async def register(user: User):
    user_repository = UserRepository()
    user_repository.create(user)
    await send_confirmation_email(user.email, user.username)
    return JSONResponse(status_code=200, content={"message": "User registered successfully. Please check your email for confirmation."})


@router.get("/confirm-email/{token}")
async def confirm_email(token: str):
    try:
        email = serializer.loads(token, salt="email-confirmation-salt", max_age=3600)  # Token válido por 1 hora
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_repo = UserRepository()
    user = user_repo.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_repo.update({"email": email}, {"$set": {"is_confirmed": True}})
    return {"message": "Email confirmed successfully"}
