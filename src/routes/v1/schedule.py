from models import CreateScheduleRequest, GetSchedulesResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from services.auth_service import AuthService
from repositories import ScheduleRepository
from typing import List
from typing import Optional

router = APIRouter(prefix="/v1", tags=["Schedules"])

@router.get("/schedules", response_model=List[GetSchedulesResponse])
async def get_schedules(
    date: Optional[str] = Query(None, description="Data no formato YYYY-MM-DD"),
    user_id: str = Depends(AuthService.verify_token)
    ):
    try:
        user_repo = ScheduleRepository()
        schedules = user_repo.get_schedules(user_id, date)
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
        return {"message": "Schedule created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
