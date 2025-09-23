from flask import Blueprint, request, jsonify
from .. import mongo
from ..schemas import user_schema  # only if using Marshmallow

users = Blueprint("users", __name__)

@users.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    mongo.db.users.insert_one(data)
    return jsonify({"msg": "User created"}), 201

@users.route("/users", methods=["GET"])
def get_users():
    users_list = list(mongo.db.users.find({}, {"_id": 0}))
    return jsonify(users_list), 200
