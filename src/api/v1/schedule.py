from ..models.schedule import CreateScheduleRequest, GetSchedulesResponse
from fastapi import APIRouter, Depends, HTTPException, status
from services.auth_service import AuthService
from db.repositories import ScheduleRepository
from typing import List

router = APIRouter(prefix="/v1", tags=["Schedules"])

@router.get("/schedules", response_model=List[GetSchedulesResponse])
async def get_schedules(user_id: str = Depends(AuthService.verify_token)):
    try:
        user_repo = ScheduleRepository()
        schedules = user_repo.get_schedules(user_id)
        if not schedules:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No schedules found for the user."
            )
        return schedules
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/schedules", status_code=status.HTTP_201_CREATED)
async def create_schedule(schedule: CreateScheduleRequest, user_id: str = Depends(AuthService.verify_token)):
    try:
        user_repo = ScheduleRepository()
        user_repo.add_schedule(user_id, schedule)
        print(user_id)
        return {"message": "Schedule created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
