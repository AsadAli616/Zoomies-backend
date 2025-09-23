from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import timedelta

from ..services.user_service import UserService
from ..schemas.user_schema import UserRegisterSchema, UserLoginSchema

auth = Blueprint("auth", __name__)

register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()


@auth.route("/register/student", methods=["POST"])
def register():
    try:
        # Validate request body
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Pass all validated fields into service layer
    user, error = UserService.register(
        email=data["email"],
        password=data["password"],
        roles="student",
        academic_level=data.get("academic_level"),
        school_institution=data.get("school_institution"),
        is_active=data.get("is_active", True),
    )

    if error:
        return jsonify({"msg": error}), 400

    return jsonify({"msg": "User registered successfully"}), 201


@auth.route("/login", methods=["POST"])
def login():
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    user, error = UserService.authenticate(data["email"], data["password"])
    if error:
        return jsonify({"msg": error}), 401

    # Create token with extra claims (roles, academic info)
    token = create_access_token(
        identity=user["email"],
        additional_claims={
            "roles": user.get("roles", []),
            "academic_level": user.get("academic_level"),
            "school_institution": user.get("school_institution"),
        },
        expires_delta=timedelta(hours=1),  # token expires in 1h
    )

    return jsonify({"token": token}), 200


@auth.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()  # email
    return jsonify({"logged_in_as": current_user}), 200
