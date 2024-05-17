from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                flash("You don’t have permissions to see this site", "warning")
                return redirect(url_for("home"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
