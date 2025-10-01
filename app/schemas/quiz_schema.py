from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class QuestionSchema(Schema):
    text = fields.String(
        required=True,
        error_messages={"required": "Question text is required."}
    )
    options = fields.List(
        fields.String(),
        required=True,
        validate=validate.Length(min=2, error="At least 2 options are required."),
        error_messages={"required": "Options are required."}
    )
    correct_answer = fields.String(
        required=True,
        error_messages={"required": "Correct answer is required."}
    )

    @validates_schema
    def validate_correct_answer(self, data, **kwargs):
        """
        Ensure correct_answer exists inside options.
        """
        if data.get("correct_answer") not in data.get("options", []):
            raise ValidationError("Correct answer must be one of the options.", field_name="correct_answer")


class QuizSchema(Schema):
    teacher_id = fields.String(
        required=True,
        error_messages={"required": "teacher id is required."}
    )
    title = fields.String(
        required=True,
        validate=validate.Length(min=3, max=200, error="Title must be between 3 and 200 characters."),
        error_messages={"required": "Title is required."}
    )
    description = fields.String(allow_none=True)

    class_level = fields.String(
        required=True,
        validate=validate.OneOf(
            ["O-level", "A-level", "SAT", "IB"],
            error="Class level must be one of: O-level, A-level, SAT, IB."
        ),
        error_messages={"required": "Class level is required."}
    )
    
    status = fields.String(
        required=True,
        validate=validate.OneOf(
            ["easy", "medium", "hard"],
            error="status  must be one of: easy, medium, hard."
        ),
        error_messages={"required": "status  is required."}
    )
    Subject = fields.String(
            required=True,
            validate=validate.OneOf(
                ["Mathematics", "Biology", "Chemistry", "Physics", "English"],
                error="status  must be one of: easy, medium, hard."
            ),
            error_messages={"required": "Subject  is required."}
        )



    quiz_type = fields.String(
        required=True,
        validate=validate.OneOf(
            ["anytime", "scheduled"],
            error="quiz type  must be one of: scheduled, anytime."
        ),
        error_messages={"required": "quiz type is required."}
    )

    start_time = fields.DateTime(
        required=False,
        error_messages={"required": "Start time is required (ISO 8601 format)."}
    )
    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error="Duration must be at least 1 minute."),
        error_messages={"required": "Duration is required."}
    )

    questions = fields.List(
        fields.Nested(QuestionSchema),
        required=True,
        validate=validate.Length(min=1, error="At least one question is required."),
        error_messages={"required": "Questions are required."}
    )

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
