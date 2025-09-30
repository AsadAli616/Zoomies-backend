from datetime import datetime, timezone
from .. import mongo

class User:
    def __init__(
        self,
        email,
        password,
        roles,
        class_level=None,
        school_institution=None,
        is_active=True,
        verified_email=False,
        otp=None,
        otp_created_at=None,
        years_of_experience=None,
        location=None,
        phone_number=None,
        teaching_subjects=None,
        bio=None,
        created_at=None,
        updated_at=None
    ):
        self.email = email
        self.password = password
        self.roles = roles
        self.class_level = class_level
        self.school_institution = school_institution
        self.is_active = is_active
        self.verified_email = verified_email
        self.otp = otp
        self.otp_created_at = otp_created_at
        self.years_of_experience = years_of_experience
        self.location = location
        self.phone_number = phone_number
        self.teaching_subjects = teaching_subjects
        self.bio = bio
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def save(self):
        data = self.__dict__
        mongo.db.users.update_one({"email": self.email}, {"$set": data}, upsert=True)
        return data

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def update_user(user_id, updates: dict):
        """
        Update a user document by ID.
        Args:
            user_id (str | ObjectId): The user's MongoDB _id.
            updates (dict): Fields to update.
        Returns:
            (dict, str): (updated_user, error_message)
        """
        from bson import ObjectId

        try:
            if not ObjectId.is_valid(user_id):
                return None, "Invalid user ID"

            updates["updated_at"] = datetime.now(timezone.utc)

            result = mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": updates}
            )

            if result.matched_count == 0:
                return None, "User not found"

            updated_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            return updated_user, None

        except Exception as e:
            return None, str(e)
