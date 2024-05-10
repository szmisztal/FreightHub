from flask import render_template, redirect, url_for, flash
from . import user_bp
from app import db, bcrypt
from app.user.forms import RegistrationForm
from app.user.models import User

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
