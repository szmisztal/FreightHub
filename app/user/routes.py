from flask import render_template, redirect, url_for, flash
from flask import request
from flask_login import login_user, logout_user, current_user
from app import db, bcrypt
from . import user_bp
from .forms import RegistrationForm, LoginForm
from .models import User

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if user_exists(form.username.data, form.email.data):
            return render_template("register.html", form=form)
        user = create_user(form)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful, please login.", "success")
        return redirect(url_for("user.login"))
    return render_template("register.html", form=form)

def user_exists(username, email):
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        flash("Username or email already registered.", "error")
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
        flash("You are logged in", "error")
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Login successful.", "success")
            return redirect(next_page or url_for("home"))
        else:
            flash("Login unsuccessful. Please check email and password.", "warning")
    return render_template("login.html", form=form)

@user_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@user_bp.route("/logout/confirm", methods=["GET"])
def logout_confirm():
    return render_template("logout_confirm.html")
