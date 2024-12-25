from typing import List, Dict, Optional, Any
import bcrypt
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
        return jsonify({"error": "user not found!"}), 404


@user_routes.post("/users")
def create_user():
    data: Dict[Optional[Any]] = dict(request.json)

    if not all(key in data for key in ("name", "email", "password")):
        return jsonify({"error": "request missing a required field!"}), 400

    try:
        hashed_password = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        )
        data["password"] = hashed_password.decode("utf-8")
    except Exception:
        return jsonify({"error": "failed to hah password!"}), 500

    try:
        user_id: Any = db.users.insert_one(data).inserted_id
        return jsonify({"id": str(user_id)}), 201
    except Exception:
        return jsonify({"error": "failed to insert new user!"}), 500


@user_routes.put("/users/<int:id>")
def update_user(id: int):
    data: Optional[Any] = request.json

    updated_user: Optional[Any] = db.users.find_one_and_update(
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
        return jsonify({"error": "user not found!"}), 404


@user_routes.delete("/users/<int:id>")
def delete_user(id: int):
    result: DeleteResult = db.users.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return jsonify({"log": "user successfully deleted!"}), 200
    else:
        return jsonify({"error": "user not found!"}), 404
