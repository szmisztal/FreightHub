from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from app import db, bcrypt
from app.common.models import User
from app.common.custom_utils import send_validation_errors_to_form
from . import user_bp
from .forms import RegistrationForm, LoginForm
from .schemas import UserSchema

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle user registration.

    This route allows new users to register by filling out the registration form.
    It validates the input data, creates a new user, and adds them to the database.

    Returns:
        str: Rendered HTML template for the registration page.
    """
    form = RegistrationForm()
    schema = UserSchema()
    if request.method == "POST":
        user_data = {
            "username": form.username.data,
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "phone_number": form.phone_number.data,
            "email": form.email.data,
            "password": form.password.data,
            "role": form.role.data
        }
        try:
            result = schema.load(user_data)
            user = create_user(result)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful, you can log in.", "success")
            return redirect(url_for("user.login"))
        except ValidationError as e:
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"Register - validation error: {e}")
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.exception(f"Registration error: {e}")
            flash("Username or email is already in use, choose another.", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Registration error: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("register.html", form=form, title="Registration")

def create_user(data):
    """
    Create a new user instance.

    This function hashes the user's password and creates a new User object.

    Args:
        data (dict): Dictionary containing user data.

    Returns:
        User: A new User object.
    """
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    return User(
        username=data["username"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone_number=data["phone_number"],
        email=data["email"],
        password_hash=hashed_password,
        role=data["role"]
    )

@user_bp.route("/change_data/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user_data(id):
    """
    Edit user data.

    This route allows users to edit their own data. It validates the input data
    and updates the user's information in the database.

    Args:
        id (int): The ID of the user to be edited.

    Returns:
        str: Rendered HTML template for the user data edit page.
    """
    if current_user.id != id:
        flash("You don't have permission to edit this user's data.", "danger")
        return redirect(url_for("home"))
    user = User.query.get_or_404(id)
    form = RegistrationForm(obj=user)
    schema = UserSchema()
    if request.method == "POST":
        user_data = {
            "username": form.username.data,
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "phone_number": form.phone_number.data,
            "email": form.email.data,
            "password": form.password.data,
            "role": form.role.data
        }
        try:
            result = schema.load(user_data)
            user.username = result["username"]
            user.first_name = result["first_name"]
            user.last_name = result["last_name"]
            user.phone_number = result["phone_number"]
            user.email = result["email"]
            if form.password.data:
                hashed_password = bcrypt.generate_password_hash(result["password"]).decode("utf-8")
                user.password_hash = hashed_password
            user.role = result["role"]
            db.session.commit()
            flash("Your user data updated successfully.", "success")
            return redirect(url_for("home"))
        except ValidationError as e:
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"Edit {user} validation error: {e}")
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.exception(f"Edit {user} error: {e}")
            flash("Username or email is already in use, choose another.", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Edit {user} error: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("register.html", form=form, title="User Data Edit")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.

    This route allows users to log in by providing their email and password.
    If the credentials are correct, the user is logged in and redirected to the home page.

    Returns:
        str: Rendered HTML template for the login page.
    """
    if current_user.is_authenticated:
        flash("You are logged in", "info")
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            flash("Login successful.", "success")
            return redirect(next_page or url_for("home"))
        else:
            flash("Login unsuccessful. Please check email and password.", "warning")
    return render_template("login.html", form=form)

@user_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Handle user logout.

    This route logs out the current user and redirects them to the home page.

    Returns:
        str: Redirect to the home page.
    """
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@user_bp.route("/logout/confirm", methods=["GET"])
@login_required
def logout_confirm():
    """
    Render logout confirmation page.

    This route displays a confirmation page before logging the user out.

    Returns:
        str: Rendered HTML template for the logout confirmation page.
    """
    return render_template("logout_confirm.html")

@user_bp.route("/all", methods=["GET"])
@login_required
def users_list():
    """
    Display list of all users.

    This route fetches all users from the database and categorizes them by role (planner, dispatcher, driver).

    Returns:
        str: Rendered HTML template displaying the list of users.
    """
    users = User.query.all()
    planners = [user for user in users if user.role == "planner"]
    dispatchers = [user for user in users if user.role == "dispatcher"]
    drivers = [user for user in users if user.role == "driver"]
    return render_template("users_list.html", planners=planners, dispatchers=dispatchers, drivers=drivers)
