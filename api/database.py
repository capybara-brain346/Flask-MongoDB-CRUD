from pymongo import MongoClient


# return the collection that needs to be connected to
def get_db():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["users"]
    return db["user_info"]
