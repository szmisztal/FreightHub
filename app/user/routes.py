from flask import render_template, redirect, url_for, flash
from app import app, db
from app.user.forms import RegistrationForm
from app.user.models import User
import bcrypt

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user is None:
                hashed_password = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt())
                hashed_password = hashed_password.decode("utf-8")
                user = User(
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password_hash=hashed_password,
                    role=form.role.data
                )
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                flash("Email already registered.")
        else:
            flash("Username already taken.")
    return render_template("register.html", form=form)
