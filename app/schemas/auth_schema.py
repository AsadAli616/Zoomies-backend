from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required."}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        error_messages={
            "required": "Password is required.",
            "invalid": "Password must be a string."
        }
    )
    class_level = fields.Str(
        required=False,
        validate=validate.Length(min=2),
        allow_none=True,
        error_messages={"invalid": "Academic level must be a string."}
    )
    school_institution = fields.Str(
        required=False,
        validate=validate.Length(min=2),
        allow_none=True,
        error_messages={"invalid": "School/Institution must be a string."}
    )
    is_active = fields.Bool(required=False, load_default=True)
    

    years_of_experience = fields.Int(required=False, allow_none=True)
    location = fields.Str(required=False, allow_none=True)
    phone_number = fields.Str(required=False, allow_none=True)
    teaching_subjects = fields.List(fields.Str(), required=False, allow_none=True)
    bio = fields.Str(required=False, allow_none=True)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class VerifySchema(Schema):
    email = fields.Email(required=True)
    otp = fields.String(
        required=True,
        validate=validate.Length(equal=6),  # ✅ cleaner than lambda
        error_messages={"required": "OTP is required.", "invalid": "OTP must be 6 digits."}
    )

class ResendOTPSchema(Schema):
    email = fields.Email(required=True)

class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)

class ResetPasswordSchema(Schema):
    email = fields.Email(required=True)
    otp = fields.String(required=True, validate=lambda x: len(x) == 6)
    new_password = fields.Str(required=True, validate=lambda x: len(x) >= 6)