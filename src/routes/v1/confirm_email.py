from core.config import SERIALIZER
from repositories import UserRepository
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/v1")

@router.get("/confirm-email/{token}")
async def confirm_email(token: str):
    try:
        email = SERIALIZER.loads(token, salt="email-confirmation-salt", max_age=3600)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_repo = UserRepository()
    user = user_repo.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_confirmed:
        return {"message": "Email already confirmed"}

    user_repo.update({"email": email}, {"$set": {"is_confirmed": True}})
    return {"message": "Email confirmed successfully"}
