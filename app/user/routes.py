from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt
from app.common.models import User
from . import user_bp
from .forms import RegistrationForm, LoginForm

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            if user_exists(form.username.data, form.email.data):
                flash("Username or email already registered.", "warning")
                return render_template("register.html", form=form)
            user = create_user(form)
            db.session.add(user)
            db.session.commit()
            flash("Registration successfully, you can log in.", "success")
            return redirect(url_for("user.login"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Registration error: {e}")
            flash(f"Error: {e}, try again", "danger")
            return redirect(url_for("home"))
    return render_template("register.html", form=form)

def user_exists(username, email):
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return True
    return False

def create_user(form):
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    return User(
        username=form.username.data,
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        email=form.email.data,
        password_hash=hashed_password,
        role=form.role.data
    )

@user_bp.route("/login", methods=["GET", "POST"])
def login():
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
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@user_bp.route("/logout/confirm", methods=["GET"])
@login_required
def logout_confirm():
    return render_template("logout_confirm.html")

@user_bp.route("/all", methods=["GET"])
@login_required
def users_list():
    users = User.query.all()
    planners = [user for user in users if user.role == "planner"]
    dispatchers = [user for user in users if user.role == "dispatcher"]
    drivers = [user for user in users if user.role == "driver"]
    return render_template("users_list.html", planners=planners, dispatchers=dispatchers, drivers=drivers)
