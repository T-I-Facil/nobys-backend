from client import get_db

class InvoiceRepository:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["invoices"]
    
    def create(self, invoice):
        return self.collection.insert_one(invoice)
    
    def get_all(self, user_id: str):
        return self.collection.find({"user_id": user_id})