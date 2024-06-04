from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Email, DataRequired

class RegistrationForm(FlaskForm):
    username = StringField("Username")
    first_name = StringField("First name")
    last_name = StringField("Last name")
    phone_number = StringField("Phone number")
    email = StringField("Email")
    password = PasswordField("Password")
    role = SelectField("Role", choices=[("planner", "Planner"),
                                        ("dispatcher", "Dispatcher"),
                                        ("driver", "Driver")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
