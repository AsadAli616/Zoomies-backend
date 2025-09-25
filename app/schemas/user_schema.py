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
    academic_level = fields.Str(
        required=False,
        validate=validate.Length(min=2),
        error_messages={"invalid": "Academic level must be a string."}
    )
    school_institution = fields.Str(
        required=False,
        validate=validate.Length(min=2),
        error_messages={"invalid": "School/Institution must be a string."}
    )
    is_active = fields.Bool(required=False, load_default=True)


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

