from mongo.client import get_db
from models.doctor import Doctor

class UserRepository:    
    def __init__(self):
        self.db = get_db()

    def create(self, user: Doctor):
        user = self.db.users.insert_one(user.model_dump())
        return {"user_id": str(user.inserted_id)}

    
    def get_by_username(self, username: str):
        user = self.db.users.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])
        return user
