from repositories import UserRepository
from core.config import SERIALIZER, CONF
from fastapi_mail import FastMail, MessageSchema

class CreateAccountService:
    def __init__(self):
        self.user_repo = UserRepository()

    def create(self, user: dict):
        return self.user_repo.create(user)
    
    async def send_confirmation_email(self, email: str, username: str):
        TOKEN = SERIALIZER.dumps(email, salt="email-confirmation-salt")
        message = MessageSchema(
            subject="Confirm Your Email",
            recipients=[email],
            body=f"Hello {username},\n\nPlease confirm your email by clicking the link below:\n\nhttp://localhost:8000/confirm-email/{TOKEN}",
            subtype="plain",
        )

        fm = FastMail(CONF)
        await fm.send_message(message)