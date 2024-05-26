from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
from app import db
from app.common.models import User, TransportationOrder, Trailer
from .models import TractorHead

class TractorHeadForm(FlaskForm):
    brand = StringField("Brand", validators=[DataRequired()])
    registration_number = StringField("Registration Number", validators=[DataRequired()])
    submit = SubmitField("Submit")

class TrailerForm(FlaskForm):
    type = SelectField("Type", choices=[("Curtain side", "Curtain-side trailer"),
                                        ("Refrigerated", "Refrigerated trailer"),
                                        ("Tipper", "Tipper trailer"),
                                        ("Low loader","Low-loader trailer"),
                                        ("Container", "Container trailer"),
                                        ("Self-unloading", "Self-unloading trailer"),
                                        ("Insulated", "Insulated trailer")],
                               validators=[DataRequired()])
    registration_number = StringField("Registration Number", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AssignDriverForm(FlaskForm):
    driver = SelectField("Driver", choices=[], validators=[DataRequired()])
    tractor_head = SelectField("Tractor Head", choices=[], validators=[DataRequired()])
    trailer = SelectField("Trailer", choices=[], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(AssignDriverForm, self).__init__(*args, **kwargs)
        self.driver.choices = [(0, "No Driver")] + [(u.id, f"{u.first_name} {u.last_name}") for u in self.get_available_drivers()]
        self.tractor_head.choices = [(0, "No Tractor head")] + [(t.id, f"{t.registration_number}") for t in self.get_available_tractor_heads()]

    def get_available_drivers(self):
        active_driver_ids = db.session.query(TransportationOrder.driver).filter(
            TransportationOrder.completed == False,
            TransportationOrder.driver.isnot(None)
        ).distinct().subquery()
        available_drivers = User.query.filter(User.role == "driver", User.id.notin_(active_driver_ids) ).all()
        return available_drivers

    def get_available_tractor_heads(self):
        active_tractor_heads_ids = db.session.query(TransportationOrder.tractor_head).filter(
            TransportationOrder.completed == False,
            TransportationOrder.tractor_head.isnot(None)
        ).distinct().subquery()
        available_tractor_heads = TractorHead.query.filter(TractorHead.id.notin_(active_tractor_heads_ids)).all()
        return available_tractor_heads
