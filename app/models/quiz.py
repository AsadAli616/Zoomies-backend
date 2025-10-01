from datetime import datetime, timezone
from bson import ObjectId
from .. import mongo

class Quiz:
    def __init__(
        self,
        teacher_id,
        title,
        class_level,
        quiz_type,
        questions,
        status,
        Subject,
        description=None,
        start_time=None,
        duration_minutes=None,
        created_at=None,
        updated_at=None
    ):
        self.teacher_id = ObjectId(teacher_id) if teacher_id else None
        self.title = title
        self.status = status
        self.description = description
        self.class_level = class_level  # ["O-level", "A-level", "SAT", "IB"]
        self.quiz_type = quiz_type      # "anytime" | "scheduled"
        self.start_time = start_time 
        self.Subject  = Subject   # datetime (only if scheduled)
        self.duration_minutes = duration_minutes  # int (only if scheduled)
        self.questions = questions      # Array of {text, options[], correct_answer}
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def save(self):
        """
        Insert or update a quiz in MongoDB.
        If title already exists for the same teacher, update it.
        """
        data = self.__dict__.copy()

        result = mongo.db.quizzes.update_one(
            {"title": self.title, "teacher_id": self.teacher_id},
            {"$set": data},
            upsert=True
        )

        if result.upserted_id:
            data["_id"] = result.upserted_id
        else:
            existing = mongo.db.quizzes.find_one(
                {"title": self.title, "teacher_id": self.teacher_id}
            )
            if existing:
                data["_id"] = existing["_id"]

        return data
    @staticmethod
    def find_paginated(skip=0, limit=10, query=None, projection=None, base_filter=None):
        """
        Fetch quizzes with pagination and return total count.
        :param skip: Number of docs to skip
        :param limit: Max docs to return
        :param query: Optional filter dict
        :param projection: Fields to include/exclude
        :param base_filter: Default WHERE clause (applied in all cases)
        :return: dict with quizzes list and total count
        """
        # base filter always applies
        if base_filter is None:
            base_filter = {}

        # merge base filter + user filter
        if query is None:
            query = {}

        final_query = {**base_filter, **query}

        total = mongo.db.quizzes.count_documents(final_query)

        cursor = (
            mongo.db.quizzes
            .find(final_query, projection)
            .skip(skip)
            .limit(limit)
        )

        return {
            "items": list(cursor),
            "total": total
        }
    
    @staticmethod
    def find_by_id(quiz_id):
        if not ObjectId.is_valid(quiz_id):
            return None
        return mongo.db.quizzes.find_one({"_id": ObjectId(quiz_id)})

    @staticmethod
    def find_all():
        return list(mongo.db.quizzes.find())

    @staticmethod
    def update_quiz(quiz_id, updates: dict):
        try:
            if not ObjectId.is_valid(quiz_id):
                return None, "Invalid quiz ID"

            updates["updated_at"] = datetime.now(timezone.utc)

            result = mongo.db.quizzes.update_one(
                {"_id": ObjectId(quiz_id)},
                {"$set": updates}
            )

            if result.matched_count == 0:
                return None, "Quiz not found"

            updated_quiz = mongo.db.quizzes.find_one({"_id": ObjectId(quiz_id)})
            return updated_quiz, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete_quiz(quiz_id):
        if not ObjectId.is_valid(quiz_id):
            return False, "Invalid quiz ID"

        result = mongo.db.quizzes.delete_one({"_id": ObjectId(quiz_id)})
        if result.deleted_count == 0:
            return False, "Quiz not found"
        return True, None
