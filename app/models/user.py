from datetime import datetime
from .. import mongo

class User:
    collection = mongo.db.users

    def __init__(
        self,
        email,
        password,
        roles=None,
        academic_level=None,
        school_institution=None,
        is_active=True,
        verified_email = False,
        otp=None
    ):
        self.email = email
        self.password = password  # already hashed in service
        self.roles = roles or ["student"]  # default role
        self.academic_level = academic_level
        self.school_institution = school_institution
        self.is_active = is_active
        self.verified_email = verified_email
        self.otp = otp
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """Insert user document into MongoDB."""
        user_data = {
            "email": self.email,
            "password": self.password,   # already hashed
            "roles": self.roles,
            "academic_level": self.academic_level,
            "school_institution": self.school_institution,
            "is_active": self.is_active,
            "verified_email": self.verified_email,
            "otp": self.otp,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        User.collection.insert_one(user_data)
        return user_data

    @staticmethod
    def find_by_email(email):
        """Find a user by email."""
        return User.collection.find_one({"email": email})
