from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date
from .custom_utils import not_blank

class TransportationOrderSchema(Schema):
    """
    Schema for validating transportation order data.

    This schema ensures that all required fields for a transportation order are present
    and conform to specified constraints.

    Attributes:
        creation_date (date): The date the order was created.
        created_by (int): The ID of the user who created the order.
        planned_delivery_date (date): The planned delivery date for the order.
        trailer_type (str): The type of trailer required for the order.
        tractor_head (int): The ID of the assigned tractor head (nullable).
        trailer (int): The ID of the assigned trailer (nullable).
        load_weight (int): The weight of the load.
        loading_place (int): The ID of the company where the load will be loaded.
        delivery_place (int): The ID of the company where the load will be delivered.
        driver (int): The ID of the assigned driver (nullable).
        completed (bool): Whether the order has been completed.
    """
    creation_date = fields.Date(required=True)
    created_by = fields.Int(required=True)
    planned_delivery_date = fields.Date(required=True, validate=[not_blank])
    trailer_type = fields.Str(required=True, validate=[validate.Length(max=16), not_blank])
    tractor_head = fields.Int(allow_none=True)
    trailer = fields.Int(allow_none=True)
    load_weight = fields.Int(required=True, validate=[validate.Range(min=1, max=24000), not_blank])
    loading_place = fields.Int(required=True, validate=[not_blank])
    delivery_place = fields.Int(required=True, validate=[not_blank])
    driver = fields.Int(allow_none=True)
    completed = fields.Bool(default=False)

    @validates("planned_delivery_date")
    def validate_planned_delivery_date(self, value):
        """
        Validate the planned delivery date.

        This method ensures that the planned delivery date is not in the past.

        Args:
            value (date): The planned delivery date to validate.

        Raises:
            ValidationError: If the planned delivery date is in the past.
        """
        if value < date.today():
            raise ValidationError("The date must be in the future.")

