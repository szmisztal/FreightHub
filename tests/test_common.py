from datetime import datetime
import pytest
from marshmallow import ValidationError

# SCHEMAS

def test_valid_date(transportation_order_schema):
    data = {
        "creation_date": str(datetime.today().date()),
        "created_by": 1,
        "planned_delivery_date": str(datetime(2222, 1, 1).date()),
        "trailer_type": "Container",
        "tractor_head": 2,
        "trailer": 3,
        "load_weight": 24000,
        "loading_place": 4,
        "delivery_place": 5,
        "driver": 6,
        "completed": False
    }
    result = transportation_order_schema.load(data)
    result["creation_date"] = str(result["creation_date"])
    result["planned_delivery_date"] = str(result["planned_delivery_date"])
    assert result == data

def test_missing_fields(transportation_order_schema):
    data = {"completed": False}
    with pytest.raises(ValidationError) as excinfo:
        transportation_order_schema.load(data)
    assert "creation_date" in excinfo.value.messages
    assert "created_by" in excinfo.value.messages
    assert "planned_delivery_date" in excinfo.value.messages
    assert "trailer_type" in excinfo.value.messages
    assert "load_weight" in excinfo.value.messages
    assert "loading_place" in excinfo.value.messages
    assert "delivery_place" in excinfo.value.messages

def test_min_load_weight(transportation_order_schema):
    data = {
        "creation_date": str(datetime.today().date()),
        "created_by": 1,
        "planned_delivery_date": str(datetime(2222, 1, 1).date()),
        "trailer_type": "Container",
        "tractor_head": 2,
        "trailer": 3,
        "load_weight": 0,
        "loading_place": 4,
        "delivery_place": 5,
        "driver": 6,
        "completed": False
    }
    with pytest.raises(ValidationError) as excinfo:
        transportation_order_schema.load(data)
    assert "load_weight" in excinfo.value.messages

def test_max_load_weight(transportation_order_schema):
    data = {
        "creation_date": str(datetime.today().date()),
        "created_by": 1,
        "planned_delivery_date": str(datetime(2222, 1, 1).date()),
        "trailer_type": "Container",
        "tractor_head": 2,
        "trailer": 3,
        "load_weight": 25000,
        "loading_place": 4,
        "delivery_place": 5,
        "driver": 6,
        "completed": False
    }
    with pytest.raises(ValidationError) as excinfo:
        transportation_order_schema.load(data)
    assert "load_weight" in excinfo.value.messages

def test_past_planned_delivery_date(transportation_order_schema):
    data = {
        "creation_date": str(datetime.today().date()),
        "created_by": 1,
        "planned_delivery_date": str(datetime(2000, 1, 1).date()),
        "trailer_type": "Container",
        "tractor_head": 2,
        "trailer": 3,
        "load_weight": 24000,
        "loading_place": 4,
        "delivery_place": 5,
        "driver": 6,
        "completed": False
    }
    with pytest.raises(ValidationError) as excinfo:
        transportation_order_schema.load(data)
    assert "planned_delivery_date" in excinfo.value.messages
