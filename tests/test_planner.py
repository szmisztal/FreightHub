import pytest
from marshmallow import ValidationError

# SCHEMAS

def test_valid_data(company_schema):
    data = {
        "company_name": "Test Company",
        "country": "Poland",
        "town": "Warsaw",
        "postal_code": "00-000",
        "street": "Test Street",
        "street_number": 1,
        "phone_number": "123456789"
    }
    result = company_schema.load(data)
    assert result == data

def test_missing_fields(company_schema):
    data = {}
    with pytest.raises(ValidationError) as excinfo:
        company_schema.load(data)
    assert "company_name" in excinfo.value.messages
    assert "country" in excinfo.value.messages
    assert "town" in excinfo.value.messages
    assert "postal_code" in excinfo.value.messages
    assert "street" in excinfo.value.messages
    assert "street_number" in excinfo.value.messages
    assert "phone_number" in excinfo.value.messages

def test_phone_number(company_schema):
    data = {
        "company_name": "Test Company",
        "country": "Poland",
        "town": "Warsaw",
        "postal_code": "00-000",
        "street": "Test Street",
        "street_number": 1,
        "phone_number": "ABCDEFGHI"
    }
    with pytest.raises(ValidationError) as excinfo:
        company_schema.load(data)
    assert "phone_number" in excinfo.value.messages
