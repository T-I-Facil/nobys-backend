from itsdangerous import URLSafeTimedSerializer
from fastapi_mail import ConnectionConfig
from fastapi.security import OAuth2PasswordBearer
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/v1/login")

MONGODB_URI = getenv("MONGODB_URI")
DB_NAME = "Nobys-Patients"
MAIL_PASSWORD = getenv("MAIL_PASSWORD")

CONF = ConnectionConfig(
    MAIL_USERNAME="shadyrajaab@gmail.com",
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM="shadyrajaab@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

SERIALIZER = URLSafeTimedSerializer("secret-key")