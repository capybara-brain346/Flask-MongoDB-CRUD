from typing import List, Dict, Optional, Any
from flask import Blueprint, jsonify, request
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from pymongo.results import DeleteResult
from database import get_db


user_routes = Blueprint("user_routes", __name__)
db = get_db()


@user_routes.get("/users")
def get_users():
    limit: Optional[str] = request.args.get("limit")
    users: Cursor = db.users.find(batch_size=int(limit))

    user_list: List[Dict[str, str]] = [
        {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
        for user in users
    ]

    return jsonify(user_list)


@user_routes.get("/users/<int:id>")
def get_user(id: int):
    user: Optional[Any] = db.users.find_one({"_id": ObjectId(id)})

    if user:
        return jsonify(
            {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
        )
    else:
        return jsonify({"error": "User not found"}), 404


@user_routes.post("/users")
def create_user():
    data: Optional[Any] = request.json

    if not all(key in data for key in ("name", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    user_id: Any = db.users.insert_one(data).inserted_id
    return jsonify({"id": str(user_id)}), 201


@user_routes.put("/users/<int:id>")
def update_user(id: int):
    data: Optional[Any] = request.json

    updated_user: Any = db.users.find_one_and_update(
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
    else:
        return jsonify({"error": "User not found"}), 404


@user_routes.delete("/users/<int:id>")
def delete_user(id: int):
    result: DeleteResult = db.users.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return jsonify({"message": "User deleted"}), 200
    else:
        return jsonify({"error": "User not found"}), 404
