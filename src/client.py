from pymongo import MongoClient

from core.config import DB_NAME, MONGODB_URI

def get_db():
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME] 
    return db