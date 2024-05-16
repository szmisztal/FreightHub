from flask import Blueprint

dispatcher_bp = Blueprint("dispatcher", __name__, template_folder="templates")

from . import routes
