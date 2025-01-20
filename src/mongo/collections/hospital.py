from mongo.client import get_db
from models.hospital import Hospital

class HospitalRepository:
    def __init__(self):
        self.db = get_db()

    def create(self, hospital: Hospital):
        return self.db.hospitals.insert_one(hospital.model_dump())
    
    def get_all(self):
        hospitals = self.db.hospitals.find()
        return [
            {**hospital, "_id": str(hospital["_id"])}
            for hospital in hospitals
        ]
