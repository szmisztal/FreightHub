from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.user import user_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "remember_to_add_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

app.register_blueprint(user_bp, url_prefix="/user")

from app.user import routes
