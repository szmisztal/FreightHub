from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = None
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "remember_to_add_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    global migrate
    migrate = Migrate(app, db)

    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    from app.user import user_bp
    from app.planner import planner_bp
    from app.dispatcher import dispatcher_bp
    from app.driver import driver_bp

    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(planner_bp, url_prefix="/planner")
    app.register_blueprint(dispatcher_bp, url_prefix="/dispatcher")
    app.register_blueprint(driver_bp, url_prefix="/driver")

    from app.common.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
