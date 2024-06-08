from flask import Blueprint

# Create a Blueprint instance for the driver module
driver_bp = Blueprint("driver", __name__, template_folder="templates")

from . import routes
