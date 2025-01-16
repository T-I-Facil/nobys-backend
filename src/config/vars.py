import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv("MONGODB_URI")
    DB_NAME = "Nobys-Patients"
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")