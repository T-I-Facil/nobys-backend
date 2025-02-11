from datetime import datetime, timedelta
import secrets
from db.client import get_db

class SessionRepository:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["sessions"]

    def create_session(self, user_id, expiration_minutes=30):
        token = secrets.token_hex(16)
        expires_at = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        session = {"token": token, "user_id": user_id, "expires_at": expires_at}
        self.collection.insert_one(session)
        return session

    def get_session(self, token):
        session = self.collection.find_one({"token": token})
        if session and session["expires_at"] > datetime.utcnow():
            return session
        return None

    def delete_session(self, token):
        self.collection.delete_one({"token": token})
