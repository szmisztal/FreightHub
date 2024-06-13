from marshmallow import Schema, fields, validate
from app.common.custom_utils import not_blank

class TractorHeadSchema(Schema):
    """
    Schema for validating tractor head data.

    This schema ensures that all required fields for a tractor head are present
    and conform to specified constraints.

    Attributes:
        brand (str): The brand of the tractor head.
        registration_number (str): The unique registration number of the tractor head.
    """
    brand = fields.Str(required=True, validate=[not_blank])
    registration_number = fields.Str(required=True, validate=[validate.Length(equal=8), not_blank])

class TrailerSchema(Schema):
    """
    Schema for validating trailer data.

    This schema ensures that all required fields for a trailer are present
    and conform to specified constraints.

    Attributes:
        type (str): The type of the trailer.
        max_load_capacity (int): trailer`s maximum load capacity.
        registration_number (str): The unique registration number of the trailer.
    """
    type = fields.Str(required=True, validate=[validate.OneOf([
        "Tanker",
        "Curtain side",
        "Refrigerated",
        "Tipper",
        "Low loader",
        "Container",
        "Self-unloading",
        "Insulated"
    ]), not_blank])
    max_load_capacity = fields.Int(required=True, validate=[not_blank])
    registration_number = fields.Str(required=True, validate=[validate.Length(equal=7), not_blank])


