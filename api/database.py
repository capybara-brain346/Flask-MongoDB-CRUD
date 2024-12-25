import os
from pymongo import MongoClient


def get_db():
    client = MongoClient(os.getenv("MONGO_DB_PATH"))
    return client["users"]
