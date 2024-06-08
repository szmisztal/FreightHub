from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from app.common.custom_utils import create_logger

# Initialize Flask extensions
db = SQLAlchemy()
migrate = None
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    """
    Create and configure an instance of the Flask application.

    This function sets up the Flask app with necessary configurations, initializes
    Flask extensions, and registers blueprints for different modules.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "remember_to_add_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize Flask extensions with the app
    db.init_app(app)
    global migrate
    migrate = Migrate(app, db)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    # Register blueprints for different modules
    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix="/user")

    from app.planner import planner_bp
    app.register_blueprint(planner_bp, url_prefix="/planner")

    from app.dispatcher import dispatcher_bp
    app.register_blueprint(dispatcher_bp, url_prefix="/dispatcher")

    from app.driver import driver_bp
    app.register_blueprint(driver_bp, url_prefix="/driver")

    from app.common.models import User

    @login_manager.user_loader
    def load_user(user_id):
        """
        Load a user by their user ID.

        Args:
            user_id (int): The ID of the user to be loaded.

        Returns:
            User: The user object corresponding to the provided user ID.
        """
        return User.query.get(int(user_id))

    # Create a logger for the application
    create_logger(app, "logs", "app.log")

    return app
