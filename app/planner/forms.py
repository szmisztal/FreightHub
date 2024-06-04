from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, DateField
from wtforms.validators import Length, DataRequired, NumberRange
from app.common.models import Trailer
from .models import Company

class CompanyForm(FlaskForm):
    company_name = StringField("Company name")
    country = StringField("Country")
    town = StringField("Town")
    postal_code = StringField("Postal code")
    street = StringField("Street")
    street_number = IntegerField("Street number")
    phone_number = StringField("Phone number")
    submit = SubmitField("Submit")

class TransportationOrderForm(FlaskForm):
    planned_delivery_date = DateField("Planned delivery date")
    trailer_type = SelectField("Trailer type", choices=[])
    load_weight = IntegerField("Load weight")
    loading_place = SelectField("Loading place", choices=[])
    delivery_place = SelectField("Delivery place", choices=[])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(TransportationOrderForm, self).__init__(*args, **kwargs)
        self.loading_place.choices = [(c.id, c.company_name) for c in Company.query.all()]
        self.delivery_place.choices = [(c.id, c.company_name) for c in Company.query.all()]
        self.trailer_type.choices = list(set([t.type for t in Trailer.query.all()]))
