from pydantic import BaseModel

class GetAnalyticsRequest(BaseModel):
    start_date: str
    end_date: str