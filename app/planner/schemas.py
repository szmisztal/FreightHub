from marshmallow import Schema, fields, validate, validates, ValidationError

class CompanySchema(Schema):
    company_name = fields.Str(required=True, validate=validate.Length(max=32))
    country = fields.Str(required=True, validate=validate.Length(max=32))
    town = fields.Str(required=True, validate=validate.Length(max=32))
    postal_code = fields.Str(required=True, validate=validate.Length(max=8))
    street = fields.Str(required=True, validate=validate.Length(max=32))
    street_number = fields.Int(required=True)
    phone_number = fields.Str(required=True, validate=validate.Length(min=8, max=32))

    @validates("phone_number")
    def validate_phone_number(self, value):
        if not value.isdigit() and not (value.startswith('+') and value[1:].isdigit()):
            raise ValidationError("Phone number must contain only digits and optional leading '+'.")

class PlannerTransportationOrderSchema(Schema):
    creation_date = fields.Date(required=True)
    created_by = fields.Int(required=True)
    planned_delivery_date = fields.Date(required=True)
    trailer_type = fields.Str(required=True, validate=validate.Length(max=16))
    tractor_head = fields.Int(allow_none=True)
    trailer = fields.Int(allow_none=True)
    load_weight = fields.Int(required=True, validate=validate.Range(min=1, max=24000))
    loading_place = fields.Int(required=True)
    delivery_place = fields.Int(required=True)
    driver = fields.Int(allow_none=True)
    completed = fields.Bool(default=False)
