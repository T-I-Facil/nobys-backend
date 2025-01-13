from pymongo import MongoClient

from config.vars import Config

def get_db():
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.DB_NAME] 
    return db