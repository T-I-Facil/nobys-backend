from repositories import InvoiceRepository, ScheduleRepository
from models import CreateInvoiceRequest, ScheduleIds, GetInvoicesResponse
from datetime import datetime

class InvoiceService:
    def __init__(self):
        self.invoice_repository = InvoiceRepository()
        self.schedule_repository = ScheduleRepository()

    def add_invoice(self, user_id: str, schedule_ids: ScheduleIds):
        total = 0
        for schedule_id in schedule_ids.schedule_ids:
            schedule = self.schedule_repository.get_schedule_by_id(schedule_id)
            total += schedule.value * schedule.schedule_time
            self.schedule_repository.update_schedule(schedule_id, {"invoiced": True})

        invoice = CreateInvoiceRequest(
            user_id=user_id,
            total=total,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            schedule_ids=schedule_ids.schedule_ids
        )
        
        return self.invoice_repository.create(invoice.model_dump())
    

    def get_invoices(self, user_id: str):
        data = self.invoice_repository.get_all(user_id)
        invoices = [
            GetInvoicesResponse(
                id=str(invoice["_id"]),
                user_id=str(invoice["user_id"]),
                total=invoice["total"],
                created_at=invoice["created_at"]
            ) for invoice in data
        ]
        return invoices
