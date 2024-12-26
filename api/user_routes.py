from typing import Optional
import bcrypt
from database import get_db
from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId


user_routes = Blueprint("user_routes", __name__)
db = get_db()


# route to retrieve all users
@user_routes.get("/users")
def get_users():
    limit: Optional[str] = request.args.get(
        "limit"
    )  # get optional limit parameter from query string

    users = db.find().limit(int(limit)) if limit else db.find()

    # transform docs to json objs
    user_list = [
        {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
        for user in users
    ]
    return jsonify(user_list)


# route to retrieve users by id
@user_routes.get("/users/<string:id>")
def get_user(id: str):
    user = db.find_one({"_id": ObjectId(id)})  # type cast string:id to type ObjectId

    if user:
        return jsonify(
            {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
        )
    return jsonify({"error": "user not found!"}), 404


# route to create a user, injests json string with schema:
# {
#   "name":"xyz",
#   "email":"xyz@gmail.com",
#   "password":"xyzpassword123"
# }
@user_routes.post("/users")
def create_user():
    data = request.json
    if not data or not all(
        key in data for key in ("name", "email", "password")
    ):  # check if all required keys are there
        return jsonify({"error": "Request missing required fields"}), 400

    try:  # hash the password for security
        hashed_password = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        )
        data["password"] = hashed_password.decode("utf-8")
        user_id = db.insert_one(data).inserted_id
        return jsonify({"id": str(user_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# route to update a user, injests json string with schema:
# {
#   "name":"xyz",
#   "email":"xyz@gmail.com",
# }
@user_routes.put("/users/<string:id>")
def update_user(id: str):
    data = request.json
    if not data:  # NoneType check
        return jsonify({"error": "No update data provided"}), 400

    try:  # user updation
        updated_user = db.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": data}, return_document=True
        )
        if updated_user:
            return jsonify(
                {
                    "id": str(updated_user["_id"]),
                    "name": updated_user["name"],
                    "email": updated_user["email"],
                }
            )
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# route to delete users by id
@user_routes.delete("/users/<string:id>")
def delete_user(id: str):
    try:
        result = db.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({"message": "User successfully deleted"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
