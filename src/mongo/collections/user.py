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

    def get_by_email(self, email: str):
        user = self.db.users.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user
    
    def update(self, filter: dict, update: dict):
        return self.db.users.update_one(filter, update)