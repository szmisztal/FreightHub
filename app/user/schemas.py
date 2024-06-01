from marshmallow import Schema, fields, validate, validates, ValidationError

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4, max=16))
    first_name = fields.Str(required=True, validate=validate.Length(max=16))
    last_name = fields.Str(required=True, validate=validate.Length(max=16))
    phone_number = fields.Str(required=True, validate=validate.Length(min=8, max=32))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))
    role = fields.Str(required=True, validate=validate.OneOf(["planner", "dispatcher", "driver"]))

    @validates("phone_number")
    def validate_phone_number(self, value):
        if not value.isdigit() and not (value.startswith('+') and value[1:].isdigit()):
            raise ValidationError("Phone number must contain only digits and optional leading '+'.")
