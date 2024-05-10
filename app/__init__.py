from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = None
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "remember_to_add_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    global migrate
    migrate = Migrate(app, db)
    bcrypt.init_app(app)

    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix="/user")

    return app
