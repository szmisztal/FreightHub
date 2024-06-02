from marshmallow import Schema, fields, validate

class TransportationOrderSchema(Schema):
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
