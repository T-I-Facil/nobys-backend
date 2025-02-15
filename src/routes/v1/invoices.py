from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from services.invoice_service import InvoiceService
from services.auth_service import AuthService
from models import ScheduleIds

router = APIRouter(prefix="/v1")

@router.post("/invoices")
async def create_invoice(invoice: ScheduleIds, user_id: str = Depends(AuthService.verify_token)):
    invoice_service = InvoiceService()
    invoice_service.add_invoice(user_id, invoice)
    return {"message": "Invoice created successfully"}

@router.get("/invoices")
async def get_invoices(user_id: str = Depends(AuthService.verify_token)):
    invoice_service = InvoiceService()
    invoices = invoice_service.get_invoices(user_id)
    return invoices