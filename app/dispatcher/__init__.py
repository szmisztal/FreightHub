from flask import Blueprint

# Create a Blueprint instance for the dispatcher module
dispatcher_bp = Blueprint("dispatcher", __name__, template_folder="templates")

from . import routes
