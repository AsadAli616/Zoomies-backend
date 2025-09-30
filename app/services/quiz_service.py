from datetime import datetime, timezone
from bson import ObjectId
from ..models.quiz import Quiz
import math


class QuizService:
    @staticmethod
    def create_quiz(data: dict):
        """
        Create a new quiz from request data.
        """
        try:
            quiz = Quiz(
                teacher_id=data["teacher_id"],
                title=data["title"],
                class_level=data["class_level"],
                start_time=data["start_time"],  # Expect datetime object
                duration_minutes=int(data["duration_minutes"]),
                questions=data["questions"],
                description=data.get("description")
            )
            return quiz.save(), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_quiz_by_id(quiz_id: str):
        """
        Fetch a quiz by its ID.
        """
        quiz = Quiz.find_by_id(quiz_id)
        if not quiz:
            return None, "Quiz not found"
        # Convert ObjectId to string for JSON response
        quiz["_id"] = str(quiz["_id"])
        quiz["teacher_id"] = str(quiz["teacher_id"])
        return quiz, None

    @staticmethod
    def get_all_quizzes(page=1, limit=10):
        """
        Fetch all quizzes with pagination.
        """
        skip = (page - 1) * limit
        cursor = Quiz.collection().find().skip(skip).limit(limit)

        quizzes = list(cursor)
        total = Quiz.collection().count_documents({})
        total_pages = math.ceil(total / limit) if limit > 0 else 1

        # Convert ObjectId to string for JSON
        for q in quizzes:
            q["_id"] = str(q["_id"])
            q["subject_id"] = str(q["subject_id"])

        return quizzes, total, total_pages

    @staticmethod
    def update_quiz(quiz_id: str, updates: dict):
        """
        Update quiz by ID.
        """
        updated_quiz, error = Quiz.update_quiz(quiz_id, updates)
        if error:
            return None, error

        updated_quiz["_id"] = str(updated_quiz["_id"])
        updated_quiz["teacher_id"] = str(updated_quiz["teacher_id"])
        return updated_quiz, None

    @staticmethod
    def delete_quiz(quiz_id: str):
        """
        Delete a quiz by ID.
        """
        success, error = Quiz.delete_quiz(quiz_id)
        if not success:
            return False, error
        return True, None
