from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Length

class CompanyForm(FlaskForm):
    company_name = StringField("Company name", validators=[InputRequired(), Length(max=32)])
    country = StringField("Country", validators=[InputRequired()])
    town = StringField("Town", validators=[InputRequired()])
    postal_code = StringField("Postal code", validators=[InputRequired()])
    street = StringField("Street", validators=[InputRequired()])
    street_number = IntegerField("Street number", validators=[InputRequired()])
    phone_number = StringField("Phone number", validators=[InputRequired()])
    submit = SubmitField("Submit")
