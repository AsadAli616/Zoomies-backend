from flask import Blueprint, request, jsonify
from ..schemas.quiz_schema import QuizSchema
from ..services.quiz_service import QuizService
from ..utils.user_guard import role_guard

quiz_bp = Blueprint("quiz", __name__)
quiz_schema = QuizSchema()
quiz_list_schema = QuizSchema(many=True)


@quiz_bp.route("/quizzes", methods=["POST"])
@role_guard(["teacher"])
def create_quiz():
    """
    Create a new quiz (teacher only).
    Supports both 'anytime' and 'scheduled' quizzes.
    """
    json_data = request.get_json()

    # Validate schema
    errors = quiz_schema.validate(json_data)
    if errors:
        return jsonify({"errors": errors}), 400

    quiz, error = QuizService.create_quiz(json_data)
    if error:
        return jsonify({"error": error}), 400

    return quiz_schema.jsonify(quiz), 201


@quiz_bp.route("/quizzes/<quiz_id>", methods=["GET"])
def get_quiz(quiz_id):
    """
    Get a quiz by ID.
    """
    quiz, error = QuizService.get_quiz_by_id(quiz_id)
    if error:
        return jsonify({"error": error}), 404

    return quiz_schema.jsonify(quiz), 200


@quiz_bp.route("/quizzes", methods=["GET"])
def get_quizzes():
    """
    Get all quizzes with pagination.
    Query Params:
        page (int) - page number, default=1
        limit (int) - items per page, default=10
        class_level (str, optional) - filter by class level
        quiz_type (str, optional) - filter by quiz type (anytime/scheduled)
    """
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    class_level = request.args.get("class_level")
    quiz_type = request.args.get("quiz_type")

    filters = {}
    if class_level:
        filters["class_level"] = class_level
    if quiz_type:
        filters["quiz_type"] = quiz_type

    quizzes, total, total_pages = QuizService.get_all_quizzes(
        page=page, limit=limit, filters=filters
    )

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "quizzes": quiz_list_schema.dump(quizzes)
    }), 200
