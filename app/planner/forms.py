from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, DateField
from wtforms.validators import Length, DataRequired, NumberRange, ValidationError
from .models import Company

class CompanyForm(FlaskForm):
    company_name = StringField("Company name", validators=[DataRequired(), Length(max=32)])
    country = StringField("Country", validators=[DataRequired()])
    town = StringField("Town", validators=[DataRequired()])
    postal_code = StringField("Postal code", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])
    street_number = IntegerField("Street number", validators=[DataRequired()])
    phone_number = StringField("Phone number", validators=[DataRequired()])
    submit = SubmitField("Submit")

def validate_future_date(form, field):
    if field.data < date.today():
        raise ValidationError("The date must be in the future.")

class TransportationOrderForm(FlaskForm):
    planned_delivery_date = DateField("Planned delivery date", validators=[DataRequired(), validate_future_date])
    trailer_type = SelectField("Trailer type", choices=[("Curtain side", "Curtain-side trailer"),
                                                        ("Refrigerated", "Refrigerated trailer"),
                                                        ("Tipper", "Tipper trailer"),
                                                        ("Low loader","Low-loader trailer"),
                                                        ("Container", "Container trailer"),
                                                        ("Self-unloading", "Self-unloading trailer"),
                                                        ("Insulated", "Insulated trailer")],
                                               validators=[DataRequired()])
    load_weight = IntegerField("Load weight", validators=[DataRequired(), NumberRange(min=1,
                                                                                       max=24000,
                                                                                       message="Weight must be in range 1-24000")])
    loading_place = SelectField("Loading place", choices=[], validators=[DataRequired()])
    delivery_place = SelectField("Delivery place", choices=[], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(TransportationOrderForm, self).__init__(*args, **kwargs)
        self.loading_place.choices = [(c.id, c.company_name) for c in Company.query.all()]
        self.delivery_place.choices = [(c.id, c.company_name) for c in Company.query.all()]


