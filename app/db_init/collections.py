from .. import mongo   # safe because mongo is initialized in create_app()

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
                        "bsonType": "string",
                        "description": "Academic level (e.g., Undergraduate, Graduate, High School)"
                    },
                    "school_institution": {
                        "bsonType": "string",
                        "description": "School or institution name"
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
                        "bsonType": "string",
                        "description": "Temporary OTP for email verification"
                    },
                    "otp_created_at": {
                        "bsonType": "date",
                        "description": "When the OTP was created (for expiration checks)"
                    },
                    "created_at": {
                        "bsonType": "date"
                    },
                    "updated_at": {
                        "bsonType": "date"
                    }
                }
            }
        })
