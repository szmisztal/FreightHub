from marshmallow import Schema, fields, validate
from app.common.custom_utils import not_blank

class TractorHeadSchema(Schema):
    brand = fields.Str(required=True, validate=[not_blank])
    registration_number = fields.Str(required=True, validate=[validate.Length(equal=8), not_blank])

class TrailerSchema(Schema):
    type = fields.Str(required=True, validate=[validate.OneOf(["Curtain side",
                                                              "Refrigerated",
                                                              "Tipper",
                                                              "Low loader",
                                                              "Container",
                                                              "Self-unloading",
                                                              "Insulated"]), not_blank])
    registration_number = fields.Str(required=True, validate=[validate.Length(equal=7), not_blank])

