from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, DataRequired, NumberRange
from .models import Company

class CompanyForm(FlaskForm):
    company_name = StringField("Company name", validators=[InputRequired(), Length(max=32)])
    country = StringField("Country", validators=[InputRequired()])
    town = StringField("Town", validators=[InputRequired()])
    postal_code = StringField("Postal code", validators=[InputRequired()])
    street = StringField("Street", validators=[InputRequired()])
    street_number = IntegerField("Street number", validators=[InputRequired()])
    phone_number = StringField("Phone number", validators=[InputRequired()])
    submit = SubmitField("Submit")

class TransportationOrderForm(FlaskForm):
    trailer_type = SelectField("Trailer type", choices=[("Curtain side", "Curtain-side trailer"),
                                                        ("Refrigerated", "Refrigerated trailer"),
                                                        ("Tipper", "Tipper trailer"),
                                                        ("Low loader","Low-loader trailer"),
                                                        ("Container", "Container trailer"),
                                                        ("Self-unloading", "Self-unloading trailer"),
                                                        ("Insulated", "Insulated trailer")],
                                               validators=[InputRequired()])
    load_weight = IntegerField("Load weight", validators=[InputRequired(), NumberRange(min=1,
                                                                                       max=24000,
                                                                                       message="Weight must be in range 1-24000")])
    loading_place = SelectField("Loading place", choices=[], validators=[DataRequired()])
    delivery_place = SelectField("Delivery place", choices=[], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(TransportationOrderForm, self).__init__(*args, **kwargs)
        self.loading_place.choices = [(c.id, c.company_name) for c in Company.query.all()]
        self.delivery_place.choices = [(c.id, c.company_name) for c in Company.query.all()]
