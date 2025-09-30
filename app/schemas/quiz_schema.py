from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from datetime import datetime

class QuestionSchema(Schema):
    text = fields.String(required=True, description="Question text")
    options = fields.List(fields.String(), required=True, validate=validate.Length(min=2))
    correct_answer = fields.String(required=True)

    @validates_schema
    def validate_correct_answer(self, data, **kwargs):
        """
        Ensure correct_answer exists inside options.
        """
        if data["correct_answer"] not in data["options"]:
            raise ValidationError("Correct answer must be one of the options.")


class QuizSchema(Schema):
    subject_id = fields.String(required=True, description="Reference to TeachingSubject (ObjectId as string)")
    title = fields.String(required=True, validate=validate.Length(min=3, max=200))
    description = fields.String(allow_none=True)
    
    class_level = fields.String(
        required=True,
        validate=validate.OneOf(["O-level", "A-level", "SAT", "IB"]),
        description="Class/Grade level for the quiz"
    )
    
    start_time = fields.DateTime(required=True, description="Datetime when quiz starts (ISO 8601 format)")
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1), description="Quiz duration in minutes")
    
    questions = fields.List(fields.Nested(QuestionSchema), required=True, validate=validate.Length(min=1))
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
