from typing import Optional
import bcrypt
from database import get_db
from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId


user_routes = Blueprint("user_routes", __name__)
db = get_db()


@user_routes.get("/users")
def get_users():
    limit: Optional[str] = request.args.get("limit")
    users = db.find().limit(int(limit)) if limit else db.find()
    user_list = [
        {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
        for user in users
    ]
    return jsonify(user_list)


@user_routes.get("/users/<string:id>")
def get_user(id: str):
    user = db.find_one({"_id": ObjectId(id)})
    if user:
        return jsonify(
            {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
        )
    return jsonify({"error": "User not found"}), 404


@user_routes.post("/users")
def create_user():
    data = request.json
    if not data or not all(key in data for key in ("name", "email", "password")):
        return jsonify({"error": "Request missing required fields"}), 400

    try:
        hashed_password = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        )
        data["password"] = hashed_password.decode("utf-8")
        user_id = db.insert_one(data).inserted_id
        return jsonify({"id": str(user_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_routes.put("/users/<string:id>")
def update_user(id: str):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    try:
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


@user_routes.delete("/users/<string:id>")
def delete_user(id: str):
    try:
        result = db.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({"message": "User successfully deleted"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
