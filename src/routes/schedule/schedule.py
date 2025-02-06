from models import Schedule
from fastapi import APIRouter, Depends
from handlers import verify_token
from mongo import UserRepository
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/v1")

@router.get("/schedules")
async def get_schedules(user_id: str = Depends(verify_token)):
    user_repo = UserRepository()
    schedules = jsonable_encoder(user_repo.get_schedules(user_id))
    return {"schedules": schedules}

@router.post("/schedules")
async def create_schedule(schedule: Schedule, user_id: str = Depends(verify_token)):
    user_repo = UserRepository()
    user_repo.add_schedule(user_id, schedule)
    return {"message": "Schedule created successfully"}