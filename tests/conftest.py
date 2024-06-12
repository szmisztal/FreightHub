import pytest
from app import create_app, db
from app.common.models import User
from app.common.schemas import TransportationOrderSchema
from app.user.routes import create_user
from app.user.schemas import UserSchema

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "LOGIN_DISABLED": True,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def user(app):
    user_data = {
        "username": "test_username",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "phone_number": "123456789",
        "email": "test@mail.com",
        "password": "test_password",
        "role": "planner"
    }
    with app.app_context():
        user = create_user(user_data)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=user_data["email"]).first()
        return user

@pytest.fixture
def logged_in_client(client, user, app):
    with app.app_context():
        app.config["LOGIN_DISABLED"] = False
        response = client.post("/user/login", data=dict(email=user.email, password="test_password"), follow_redirects=True)
        assert response.status_code == 200
    app.config["LOGIN_DISABLED"] = True
    return client

@pytest.fixture
def user_schema():
    return UserSchema()

@pytest.fixture
def transportation_order_schema():
    return TransportationOrderSchema()
