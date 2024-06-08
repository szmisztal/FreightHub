from flask import Blueprint

# Create a Blueprint instance for the planner module
planner_bp = Blueprint("planner", __name__, template_folder="templates")

from . import routes
