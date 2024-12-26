import os
from pymongo import MongoClient


def get_db():
    client = MongoClient(os.getenv("MONGO_DB_PATH"))
    client_db = client["users"]
    return client_db["user_info"]
