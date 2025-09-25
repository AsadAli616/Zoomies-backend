from datetime import datetime
from .. import mongo
from datetime import datetime, timezone

class User:
    def __init__(self, email, password, roles, academic_level=None,
                 school_institution=None, is_active=True, verified_email=False,
                 otp=None, otp_created_at=None, created_at=None, updated_at=None):
        self.email = email
        self.password = password
        self.roles = roles
        self.academic_level = academic_level
        self.school_institution = school_institution
        self.is_active = is_active
        self.verified_email = verified_email
        self.otp = otp
        self.otp_created_at = otp_created_at
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

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
            # Ensure valid ObjectId
            if not ObjectId.is_valid(user_id):
                return None, "Invalid user ID"

            # Always update the 'updated_at' field
            updates["updated_at"] = datetime.now(timezone.utc)

            result = mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": updates}
            )

            if result.matched_count == 0:
                return None, "User not found"

            # Return the updated user
            updated_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            return updated_user, None

        except Exception as e:
            return None, str(e)