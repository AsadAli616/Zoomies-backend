import random
from datetime import datetime
from flask_mail import Message
from ..models.user import User
from .. import bcrypt, mail
from ..utils.mailer import send_otp_email


class UserService:

    @staticmethod
    def register(email, password, roles=None, academic_level=None, school_institution=None, is_active=True):
        """Register a new user, send OTP for verification, and save to DB."""
        existing_user = User.find_by_email(email)
        if existing_user:
            return None, "User already exists"

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        otp = str(random.randint(100000, 999999))

        user = User(
            email=email,
            password=hashed_pw,
            roles=roles,
            academic_level=academic_level,
            school_institution=school_institution,
            is_active=is_active,
            verified_email=False,
            otp=otp
        )

        user_data = user.save()

        success, error = send_otp_email(email, otp)
        if not success:
            return None, f"User created but email failed to send: {error}"

        return user_data, None

    @staticmethod
    def authenticate(email, password):
        """Authenticate user login. Block if email not verified."""
        user = User.find_by_email(email)
        if not user:
            return None, "User not found"

        if not bcrypt.check_password_hash(user["password"], password):
            return None, "Invalid credentials"

        if not user.get("verified_email", False):
            return None, "Email not verified. Please check your inbox for OTP."

        return user, None
