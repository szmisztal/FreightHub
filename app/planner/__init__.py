from flask import Blueprint

planner_bp = Blueprint("planner", __name__, template_folder="templates")

from . import routes
