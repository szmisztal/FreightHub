from marshmallow import Schema, fields, validate, validates, ValidationError
from app.common.custom_utils import not_blank

class CompanySchema(Schema):
    """
    Schema for validating company data.

    This schema ensures that all required fields for a company are present and
    conform to specified constraints.

    Attributes:
        company_name (str): The name of the company.
        country (str): The country where the company is located.
        town (str): The town where the company is located.
        postal_code (str): The postal code of the company's address.
        street (str): The street name of the company's address.
        street_number (int): The street number of the company's address.
        phone_number (str): The contact phone number of the company.
    """
    company_name = fields.Str(required=True, validate=[validate.Length(max=32), not_blank])
    country = fields.Str(required=True, validate=[validate.Length(max=32), not_blank])
    town = fields.Str(required=True, validate=[validate.Length(max=32), not_blank])
    postal_code = fields.Str(required=True, validate=[validate.Length(max=8), not_blank])
    street = fields.Str(required=True, validate=[validate.Length(max=32), not_blank])
    street_number = fields.Int(required=True)
    phone_number = fields.Str(required=True, validate=[validate.Length(min=8, max=32), not_blank])

    @validates("phone_number")
    def validate_phone_number(self, value):
        """
        Validate the phone number field.

        This method ensures that the phone number contains only digits, with an optional leading '+'.

        Args:
            value (str): The phone number to validate.

        Raises:
            ValidationError: If the phone number contains invalid characters.
        """
        if not value.isdigit() and not (value.startswith('+') and value[1:].isdigit()):
            raise ValidationError("Phone number must contain only digits and optional leading '+'.")

