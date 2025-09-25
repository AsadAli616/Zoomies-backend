from flask import Blueprint, request, jsonify
from .. import mongo
from ..schemas import auth_schema  # only if using Marshmallow

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def create_user():
 
    return jsonify({"msg": "User created"}), 201

