from pymongo import MongoClient


def get_db():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["users"]
    return db["user_info"]
