import pytest
from marshmallow import ValidationError

# SCHEMAS

def test_valid_tractor_head_data(tractor_head_schema):
    data = {
        "brand": "MAN",
        "registration_number": "WGM12345"
    }
    result = tractor_head_schema.load(data)
    assert result == data

def test_missing_fields_for_tractor_head(tractor_head_schema):
    data = {}
    with pytest.raises(ValidationError) as excinfo:
        tractor_head_schema.load(data)
    assert "brand" in excinfo.value.messages
    assert "registration_number" in excinfo.value.messages

def test_tractor_head_registration_number(tractor_head_schema):
    data = {
        "brand": "MAN",
        "registration_number": "WGM"
    }
    with pytest.raises(ValidationError) as excinfo:
        tractor_head_schema.load(data)
    assert "registration_number" in excinfo.value.messages

def test_trailer_data(trailer_schema):
    data = {
        "type": "Container",
        "registration_number": "WND1234"
    }
    result = trailer_schema.load(data)
    assert result == data

def test_missing_fields_for_trailer(trailer_schema):
    data = {}
    with pytest.raises(ValidationError) as excinfo:
        trailer_schema.load(data)
    assert "type" in excinfo.value.messages
    assert "registration_number" in excinfo.value.messages

def test_trailer_type(trailer_schema):
    data = {
        "type": "Invalid Type",
        "registration_number": "WND1234"
    }
    with pytest.raises(ValidationError) as excinfo:
        trailer_schema.load(data)
    assert "type" in excinfo.value.messages

def test_trailer_registration_number(tractor_head_schema):
    data = {
        "type": "Container",
        "registration_number": "WND"
    }
    with pytest.raises(ValidationError) as excinfo:
        tractor_head_schema.load(data)
    assert "registration_number" in excinfo.value.messages
