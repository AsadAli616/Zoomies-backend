from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import timedelta

from ..services.user_service import UserService
from ..schemas.auth_schema import UserRegisterSchema, UserLoginSchema , VerifySchema ,ResendOTPSchema,ForgotPasswordSchema,ResetPasswordSchema

auth = Blueprint("auth", __name__)
forgot_schema = ForgotPasswordSchema()
reset_schema = ResetPasswordSchema()
register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()
verify_schema = VerifySchema()
resend_otp_schema = ResendOTPSchema()

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
        roles=["student"],
        academic_level=data.get("academic_level"),
        school_institution=data.get("school_institution"),
        is_active=data.get("is_active", True),
    )

    if error:
        return jsonify({"msg": error}), 400

    return jsonify({"msg": "User registered successfully. Please check your email for OTP.","succes":True}), 201

@auth.route("/register/teacher", methods=["POST"])
def register_teacher():
    try:
    
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Pass all validated fields into service layer
    user, error = UserService.register(
        email=data["email"],
        password=data["password"],
        roles=["teacher"],
        academic_level=data.get("academic_level"),
        school_institution=data.get("school_institution"),
        is_active=data.get("is_active", True),
        years_of_experience=data.get("years_of_experience"),
        location=data.get("location"),
        phone_number=data.get("phone_number"),
        teaching_subjects=data.get("teaching_subjects"),
        bio=data.get("bio")
    )

    if error:
        return jsonify({"msg": error}), 400

    return jsonify({"msg": "Teacher registered successfully. Please check your email for OTP."}),200  

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
        }    )

    return jsonify({"token": token ,"user": user }), 200

@auth.route("/verify-email", methods=["POST"])
def verify_email():
    try:
        # Schema ensures `email` and `otp` are provided
        data = verify_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    user, error = UserService.verify_email(data["email"], data["otp"])
    if error:
        return jsonify({"msg": error}), 400

    token = create_access_token(
        identity=user["email"],
        additional_claims={
            "roles": user.get("roles", []),
            "academic_level": user.get("academic_level"),
            "school_institution": user.get("school_institution"),
        }
    )

    return jsonify({"msg": "Email verified successfully","token":token,"user":user}), 200

@auth.route("/forgot-password", methods=["POST"])
def forgot_password():
    try:
        data = forgot_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    res, error = UserService.forgot_password(data["email"])
    if error:
        return jsonify({"msg": error}), 400

    return jsonify(res), 200

@auth.route("/reset-password", methods=["POST"])
def reset_password():
    try:
        data = reset_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    res, error = UserService.reset_password(
        email=data["email"],
        otp=data["otp"],
        new_password=data["new_password"]
    )
    if error:
        return jsonify({"msg": error}), 400

    return jsonify(res), 200

@auth.route("/resend-otp", methods=["POST"])
def resend_otp():
    try:
        # Validate request body (only email needed)
        data = resend_otp_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    user, error = UserService.resend_otp(data["email"])
    if error:
        return jsonify({"msg": error}), 400

    return jsonify({"msg": "OTP resent successfully. Please check your email."}), 200