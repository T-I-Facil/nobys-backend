from fastapi import APIRouter
from models.doctor import Doctor
from mongo import UserRepository

router = APIRouter(prefix="/v1")

@router.post("/register")
async def register(user: Doctor):
    user_repository = UserRepository()
    return user_repository.create(user)

@router.get("/test")
async def get_user_by_name(username: str):
    user_repository = UserRepository()
    return user_repository.get_by_username(username)