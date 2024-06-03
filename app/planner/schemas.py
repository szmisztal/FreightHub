from marshmallow import Schema, fields, validate, validates, ValidationError
from app.common.custom_utils import not_blank

class CompanySchema(Schema):
    company_name = fields.Str(required=True, validate=[validate.Length(max=32), not_blank])
    country = fields.Str(required=True, validate=[validate.Length(max=32), not_blank])
    town = fields.Str(required=True, validate=[validate.Length(max=32), not_blank])
    postal_code = fields.Str(required=True, validate=[validate.Length(max=8), not_blank])
    street = fields.Str(required=True, validate=[validate.Length(max=32), not_blank])
    street_number = fields.Int(required=True)
    phone_number = fields.Str(required=True, validate=[validate.Length(min=8, max=32), not_blank])

    @validates("phone_number")
    def validate_phone_number(self, value):
        if not value.isdigit() and not (value.startswith('+') and value[1:].isdigit()):
            raise ValidationError("Phone number must contain only digits and optional leading '+'.")
