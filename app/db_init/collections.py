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
                   "class_level": {
                        "enum": ["O-level", "A-level", "SAT", "IB"],
                        "description": "Class/Grade level for the quiz"
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
    if "quizzes" not in db.list_collection_names():
        db.create_collection("quizzes", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": [
                    "teacher_id",
                    "title",
                    "class_level",
                    "quiz_type",
                    "questions",
                    "created_at"
                ],
                "properties": {
                    "teacher_id": {
                        "bsonType": "objectId",
                        "description": "Reference to User with role=teacher"
                    },
                    "title": {
                        "bsonType": "string",
                        "description": "Quiz title"
                    },
                    "description": {
                        "bsonType": ["string", "null"],
                        "description": "Optional quiz description"
                    },
                    "class_level": {
                        "enum": ["O-level", "A-level", "SAT", "IB"],
                        "description": "Class/Grade level for the quiz"
                    },
                    "quiz_type": {
                        "enum": ["anytime", "scheduled"],
                        "description": "Type of quiz: anytime (open) or scheduled"
                    },
                    "start_time": {
                        "bsonType": ["date", "null"],
                        "description": "When the quiz starts (required if scheduled)"
                    },
                     "status": {
                          "enum": ["easy", "medium", "hard"],
                       "description": "Difficulty level of the quiz"
                         },
                    "duration_minutes": {
                        "bsonType": ["int", "null"],
                        "minimum": 1,
                        "description": "Quiz duration in minutes (required if scheduled)"
                    },
                    "questions": {
                        "bsonType": "array",
                        "minItems": 1,
                        "items": {
                            "bsonType": "object",
                            "required": ["text", "options", "correct_answer"],
                            "properties": {
                                "text": {
                                    "bsonType": "string",
                                    "description": "Question text"
                                },
                                "options": {
                                    "bsonType": "array",
                                    "minItems": 2,
                                    "items": {"bsonType": "string"},
                                    "description": "Answer options (at least 2 required)"
                                },
                                "correct_answer": {
                                    "bsonType": "string",
                                    "description": "Correct answer (must be one of the options)"
                                }
                            }
                        },
                        "description": "Array of questions"
                    },
                    "created_at": {
                        "bsonType": "date",
                        "description": "Quiz creation timestamp"
                    },
                    "updated_at": {
                        "bsonType": ["date", "null"],
                        "description": "Last update timestamp"
                    }
                }
            }
        })
    if "quiz_attempts" not in db.list_collection_names():
     db.create_collection("quiz_attempts", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["quiz_id", "student_id", "answers", "submitted_at", "score"],
            "properties": {
                "quiz_id": {
                    "bsonType": "objectId",
                    "description": "Reference to quiz"
                },
                "student_id": {
                    "bsonType": "objectId",
                    "description": "Reference to student (User._id)"
                },
                "answers": {
                    "bsonType": "array",
                    "minItems": 1,
                    "items": {
                        "bsonType": "object",
                        "required": ["question_text", "selected_option", "is_correct"],
                        "properties": {
                            "question_text": {
                                "bsonType": "string",
                                "description": "Question text"
                            },
                            "selected_option": {
                                "bsonType": "string",
                                "description": "Option chosen by student"
                            },
                            "is_correct": {
                                "bsonType": "bool",
                                "description": "Was the selected answer correct?"
                            }
                        }
                    },
                    "description": "Array of student answers"
                },
                "score": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "Number of correct answers"
                },
                "submitted_at": {
                    "bsonType": "date",
                    "description": "When the student submitted the quiz"
                }
            }
        }
    })

