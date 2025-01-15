from itsdangerous import URLSafeTimedSerializer
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="shadyrajaab@gmail.com",
    MAIL_PASSWORD="nijf ztrx svzg ftyt",
    MAIL_FROM="shadyrajaab@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

serializer = URLSafeTimedSerializer("secret-key")

async def send_confirmation_email(email: str, username: str):
    token = serializer.dumps(email, salt="email-confirmation-salt")
    confirm_url = f"http://localhost:8000/v1/confirm-email/{token}"

    message = MessageSchema(
        subject="Confirm Your Email",
        recipients=[email],
        body=f"Hello {username},\n\nPlease confirm your email by clicking on the link below:\n\n{confirm_url}",
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
