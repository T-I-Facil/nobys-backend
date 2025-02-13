from pydantic import BaseModel

class ScheduleIds(BaseModel):
    schedule_ids: list

class CreateInvoiceRequest(BaseModel):
    user_id: str
    total: float
    created_at: str
    schedule_ids: list