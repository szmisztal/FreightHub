from flask import Blueprint

# Create a Blueprint instance for the user module
user_bp = Blueprint("user", __name__, template_folder="templates")

from . import routes
