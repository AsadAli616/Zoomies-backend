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
            quiz_type = data.get("quiz_type")

            # Validate conditional fields
            if quiz_type == "scheduled":
                if not data.get("start_time") or not data.get("duration_minutes"):
                    return None, "Scheduled quizzes require start_time and duration_minutes"

                # Ensure datetime parsing
                if isinstance(data["start_time"], str):
                    data["start_time"] = datetime.fromisoformat(data["start_time"].replace("Z", "+00:00"))

                duration_minutes = int(data["duration_minutes"])
            else:
                data["start_time"] = None
                duration_minutes = None

            quiz = Quiz(
                teacher_id=data["teacher_id"],
                title=data["title"],
                status=data["status"],
                class_level=data["class_level"],
                quiz_type=quiz_type,
                questions=data["questions"],
                description=data.get("description"),
                start_time=data.get("start_time"),
                Subject=data["Subject"],
                duration_minutes=duration_minutes
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

        projection = {
            "title": 1,
            "_id": 1,
            "questions": 1,
            "quiz_type": 1,
            "start_time": 1,
            "status": 1,
            "class_level": 1,
            "teacher_id": 1
        }

        quizzes = Quiz.find_paginated(skip, limit, {}, projection)

        total = quizzes.get("total", 0)
        total_pages = math.ceil(total / limit) if limit > 0 else 1

        # Convert ObjectId to string for JSON
        for q in quizzes["items"]:
            q["_id"] = str(q["_id"])
            if "teacher_id" in q:
                q["teacher_id"] = str(q["teacher_id"])

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "quizzes": quizzes["items"]
        }

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
