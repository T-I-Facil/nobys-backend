from models import Schedule
from fastapi import APIRouter
from mongo import UserRepository
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/v1")

@router.get("/schedules")
async def get_schedules(user_id: str):
    user_repo = UserRepository()
    schedules = jsonable_encoder(user_repo.get_schedules(user_id))
    return {"schedules": schedules}

@router.post("/schedules")
async def create_schedule(user_id: str, schedule: Schedule):
    user_repo = UserRepository()
    user_repo.add_schedule(user_id, schedule)
    return {"message": "Schedule created successfully"}