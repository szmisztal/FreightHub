from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(role):
    """
    Decorator to restrict access to a route based on the user's role.

    This decorator checks if the current user has the required role to access
    the decorated route. If the user does not have the required role, they are
    redirected to the home page with a flash message.

    Args:
        role (str): The required role for accessing the route.

    Returns:
        function: The decorated function.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                flash("You don’t have permissions to see this site", "warning")
                return redirect(url_for("home"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
