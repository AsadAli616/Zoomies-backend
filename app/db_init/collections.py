from .. import mongo
from datetime import datetime

def create_collections():
    db = mongo.db
    if "users" not in db.list_collection_names():
        db.create_collection("users", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["email", "password", "roles"],
                "properties": {
                    "email": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "password": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "roles": {
                        "bsonType": "array",
                        "items": {
                            "enum": ["admin", "teacher", "student"],
                            "description": "Role must be one of: admin, teacher, student"
                        }
                    },
                    "academic_level": {
                        "bsonType": ["string", "null"],
                        "description": "Academic level (optional, can be null)"
                    },
                    "school_institution": {
                        "bsonType": ["string", "null"],
                        "description": "School or institution name (optional, can be null)"
                    },
                    "is_active": {
                        "bsonType": "bool",
                        "description": "User status (active/inactive)"
                    },
                    "verified_email": {
                        "bsonType": "bool",
                        "description": "Has the user verified their email?"
                    },
                    "otp": {
                        "bsonType": ["string", "null"],
                        "description": "Temporary OTP for email verification (nullable)"
                    },
                    "otp_created_at": {
                        "bsonType": ["date", "null"],
                        "description": "When the OTP was created (nullable)"
                    },
                    "years_of_experience": {
                        "bsonType": ["int", "null"],
                        "description": "Years of experience (nullable)"
                    },
                    "location": {
                        "bsonType": ["string", "null"],
                        "description": "Location (nullable)"
                    },
                    "phone_number": {
                        "bsonType": ["string", "null"],
                        "description": "Phone number (nullable)"
                    },
                    "teaching_subjects": {
                        "bsonType": ["array", "null"],
                        "items": {"bsonType": "string"},
                        "description": "Array of subjects the teacher can teach (nullable)"
                    },
                    "bio": {
                        "bsonType": ["string", "null"],
                        "description": "Bio (nullable)"
                    },
                    "created_at": {
                        "bsonType": "date",
                        "description": "Creation timestamp"
                    },
                    "updated_at": {
                        "bsonType": "date",
                        "description": "Last update timestamp"
                    }
                }
            }
        })
