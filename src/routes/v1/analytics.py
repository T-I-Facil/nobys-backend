from fastapi import APIRouter, Depends
from services import AuthService, AnalyticsService
from models import GetAnalyticsRequest

router = APIRouter(prefix="/v1")

@router.get("/analytics")
async def analytics(start_date: str, end_date: str, user_id: str = Depends(AuthService.verify_token)):
    analytics_service = AnalyticsService()
    analytics = analytics_service.get_analytics(user_id, start_date, end_date)
    return analytics