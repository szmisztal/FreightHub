import pytest
from marshmallow import ValidationError

#PAGES

def test_registration_page(client):
    response = client.get("/user/register")
    assert response.status_code == 200
    assert b'Registration Form' in response.data

def test_login_page(client):
    response = client.get("/user/login")
    assert response.status_code == 200
    assert b'Login Form' in response.data

def test_users_list_page(logged_in_client):
    response = logged_in_client.get("/user/all")
    assert response.status_code == 200
    assert b"Users List" in response.data

# FORMS

def test_submit_registration_form(client):
    response = client.post("/user/register", data={
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "phone_number": "123456789",
        "email": "newuser@example.com",
        "password": "password",
        "role": "planner"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Registration successful, you can log in.' in response.data

def test_submit_login_form(client, user):
    response = client.post("/user/login", data={
        "email": user.email,
        "password": "test_password"
    }, follow_redirects=True)
    assert response.status_code == 200

#SCHEMAS

def test_valid_user_data(user_schema):
    data = {
        "username": "test_username",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "phone_number": "123456789",
        "email": "test@mail.com",
        "password": "test_password",
        "role": "planner"
    }
    result = user_schema.load(data)
    assert result == data

def test_invalid_username(user_schema):
    data = {
        "username": "t",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "phone_number": "123456789",
        "email": "test@mail.com",
        "password": "test_password",
        "role": "planner"
    }
    with pytest.raises(ValidationError) as excinfo:
        user_schema.load(data)
    assert "username" in excinfo.value.messages

def test_invalid_phone_number(user_schema):
    data = {
        "username": "test_username",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "phone_number": "ABCDEFGHI",
        "email": "test@mail.com",
        "password": "test_password",
        "role": "planner"
    }
    with pytest.raises(ValidationError) as excinfo:
        user_schema.load(data)
    assert "phone_number" in excinfo.value.messages

def test_invalid_email(user_schema):
    data = {
        "username": "test_username",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "phone_number": "123456789",
        "email": "test",
        "password": "test_password",
        "role": "planner"
    }
    with pytest.raises(ValidationError) as excinfo:
        user_schema.load(data)
    assert "email" in excinfo.value.messages

def test_missing_required_fields(user_schema):
    data = {
        "username": "test_username"
    }
    with pytest.raises(ValidationError) as excinfo:
        user_schema.load(data)
    assert "first_name" in excinfo.value.messages
    assert "last_name" in excinfo.value.messages
    assert "phone_number" in excinfo.value.messages
    assert "email" in excinfo.value.messages
    assert "password" in excinfo.value.messages
    assert "role" in excinfo.value.messages

def test_invalid_role(user_schema):
    data = {
        "username": "test_username",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "phone_number": "123456789",
        "email": "test@mail.com",
        "password": "test_password",
        "role": "test_role"
    }
    with pytest.raises(ValidationError) as excinfo:
        user_schema.load(data)
    assert "role" in excinfo.value.messages
