from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.create_account_service import CreateAccountService
from models import CreateUser

router = APIRouter(prefix="/v1")

@router.post("/register")
async def register(user: CreateUser):
    account_service = CreateAccountService()
    account_service.create(user)
    await account_service.send_confirmation_email(user.email, user.name)
    return JSONResponse(status_code=200, content={"message": "User registered successfully. Please check your email for confirmation."})

