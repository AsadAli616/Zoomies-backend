import random
from datetime import datetime, timezone
from flask_mail import Message
from ..models.user import User
from .. import bcrypt, mail
from ..utils.mailer import send_otp_email

class UserService:

    @staticmethod
    def register(
        email,
        password,
        roles=None,
        academic_level=None,
        school_institution=None,
        is_active=True,
        years_of_experience=None,
        location=None,
        phone_number=None,
        teaching_subjects=None,
        bio=None
    ):
        """Register a new user, send OTP for verification, and save to DB."""

        # Check if user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            return None, "User already exists"

        # Hash password
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Create user object
        user = User(
            email=email,
            password=hashed_pw,
            roles=roles,
            academic_level=academic_level,
            school_institution=school_institution,
            is_active=is_active,
            verified_email=False,
            otp=otp,
            years_of_experience=years_of_experience,
            location=location,
            phone_number=phone_number,
            teaching_subjects=teaching_subjects,
            bio=bio
        )

        # Set timezone-aware OTP creation time
        user.otp_created_at = datetime.now(timezone.utc)

        # Save user to DB
        user_data = user.save()

        # Send OTP email
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

    @staticmethod
    def verify_email(email, otp):
        """Verify user's email with OTP."""
        user = User.find_by_email(email)
        if not user:
            return None, "User not found"

        if user.get("verified_email", False):
            return None, "Email already verified"

        if user.get("otp") != otp:
            return None, "Invalid OTP"

        # Optionally check expiration (e.g., OTP valid for 10 minutes)
        created_at = user.get("otp_created_at")
        if created_at and (datetime.utcnow() - created_at).seconds > 600:
            return None, "OTP expired. Please request a new one."

        # Mark as verified
        user["verified_email"] = True
        user["otp"] = None  # Clear OTP after successful verification
        user["otp_created_at"] = None
        User.update_user(user["_id"],user)

        return user, None
    
    @staticmethod
    def resend_otp(email):
        """
        Resend a new OTP to the user's email.
        Returns (user, error_message)
        """
        user = User.find_by_email(email)
        if not user:
            return None, "User not found"

        if user.get("verified_email", False):
            return None, "Email already verified"

        # Generate new OTP
        otp = str(random.randint(100000, 999999))
        now = datetime.now(timezone.utc)

        # Use your update function instead of raw mongo
        updated_user = User.update_user(
            user["_id"],
            {
                "otp": otp,
                "otp_created_at": now,
                "updated_at": now
            }
        )

        # Send email
        success, error = send_otp_email(email, otp)
        if not success:
            return None, f"Failed to send OTP: {error}"

        return updated_user, None
    
    @staticmethod
    def forgot_password(email):
        """Generate OTP for password reset and send via email."""
        user = User.find_by_email(email)
        if not user:
            return None, "User not found"

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        now = datetime.now(timezone.utc)

        # Save OTP to user document
        User.update_user(user["_id"], {"otp": otp, "otp_created_at": now})

        # Send OTP email
        success, error = send_otp_email(email, otp, subject="Password Reset OTP")
        if not success:
            return None, f"Failed to send OTP: {error}"

        return {"msg": "OTP sent to email"}, None

    @staticmethod
    def reset_password(email, otp, new_password):
        """Verify OTP and update user password."""
        user = User.find_by_email(email)
        if not user:
            return None, "User not found"

        if user.get("otp") != otp:
            return None, "Invalid OTP"

        # Optional: check OTP expiry (e.g., 10 min)
        created_at = user.get("otp_created_at")
        if created_at and (datetime.now(timezone.utc) - created_at).seconds > 600:
            return None, "OTP expired. Request a new one."

        # Hash new password
        hashed_pw = bcrypt.generate_password_hash(new_password).decode("utf-8")

        # Update password and clear OTP
        User.update_user(user["_id"], {
            "password": hashed_pw,
            "otp": None,
            "otp_created_at": None
        })

        return {"msg": "Password reset successfully"}, None