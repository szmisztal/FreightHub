from marshmallow import Schema, fields, validate, validates, ValidationError
from app.common.custom_utils import not_blank

class UserSchema(Schema):
    username = fields.Str(required=True, validate=[validate.Length(min=4, max=16), not_blank])
    first_name = fields.Str(required=True, validate=[validate.Length(max=16), not_blank])
    last_name = fields.Str(required=True, validate=[validate.Length(max=16), not_blank])
    phone_number = fields.Str(required=True, validate=[validate.Length(min=8, max=32), not_blank])
    email = fields.Email(required=True, validate=[not_blank])
    password = fields.Str(required=True, validate=[validate.Length(min=8, max=128), not_blank])
    role = fields.Str(required=True, validate=[validate.OneOf(["planner", "dispatcher", "driver"]), not_blank])

    @validates("phone_number")
    def validate_phone_number(self, value):
        if not value.isdigit() and not (value.startswith('+') and value[1:].isdigit()):
            raise ValidationError("Phone number must contain only digits and optional leading '+'.")
