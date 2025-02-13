from pydantic import BaseModel

class Invoice(BaseModel):
    id: str
    user_id: str
    total: float
    created_at: str
    schedule_ids: list