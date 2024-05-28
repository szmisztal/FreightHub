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

class CompletingTheTransportationOrderForm(FlaskForm):
    driver = SelectField("Driver", choices=[], validators=[DataRequired()])
    tractor_head = SelectField("Tractor Head", choices=[], validators=[DataRequired()])
    trailer = SelectField("Trailer", choices=[], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(CompletingTheTransportationOrderForm, self).__init__(*args, **kwargs)

        assigned_driver = kwargs.get("obj").assigned_driver
        assigned_tractor_head = kwargs.get("obj").assigned_tractor_head
        assigned_trailer = kwargs.get("obj").assigned_trailer

        driver_choices = [(0, "No Driver")]
        if assigned_driver:
            driver_choices.append((assigned_driver.id, f"{assigned_driver.first_name} {assigned_driver.last_name}"))
        driver_choices += [(u.id, f"{u.first_name} {u.last_name}") for u in self.get_available_drivers()]
        self.driver.choices = driver_choices

        tractor_head_choices = [(0, "No Tractor Head")]
        if assigned_tractor_head:
            tractor_head_choices.append((assigned_tractor_head.id, f"{assigned_tractor_head.brand} {assigned_tractor_head.registration_number}"))
        tractor_head_choices += [(t.id, f"{t.brand} {t.registration_number}") for t in self.get_available_tractor_heads()]
        self.tractor_head.choices = tractor_head_choices

        trailer_choices = [(0, "No Trailer")]
        if assigned_trailer:
            trailer_choices.append((assigned_trailer.id, f"{assigned_trailer.registration_number}"))
        trailer_choices += [(tr.id, f"{tr.registration_number}") for tr in self.get_available_trailer(kwargs.get("obj").trailer_type)]
        self.trailer.choices = trailer_choices

    def get_available_drivers(self):
        all_drivers = User.query.filter(User.role == "driver").all()
        busy_driver_ids = db.session.query(TransportationOrder.driver).filter(
            TransportationOrder.completed == False,
            TransportationOrder.driver.isnot(None)
        ).all()
        busy_driver_ids = [driver_id for (driver_id,) in busy_driver_ids]
        available_drivers = [driver for driver in all_drivers if driver.id not in busy_driver_ids]
        return available_drivers

    def get_available_tractor_heads(self):
        all_tractor_heads = TractorHead.query.all()
        busy_tractor_head_ids = db.session.query(TransportationOrder.tractor_head).filter(
            TransportationOrder.completed == False,
            TransportationOrder.tractor_head.isnot(None)
        ).all()
        busy_tractor_head_ids = [tractor_head_id for (tractor_head_id,) in busy_tractor_head_ids]
        available_tractor_heads = [tractor_head for tractor_head in all_tractor_heads if tractor_head.id not in busy_tractor_head_ids]
        return available_tractor_heads

    def get_available_trailer(self, trailer_type):
        busy_trailer_ids = db.session.query(TransportationOrder.trailer).filter(
            TransportationOrder.completed == False,
            TransportationOrder.trailer.isnot(None)
        ).all()
        busy_trailers = [trailer_id for (trailer_id,) in busy_trailer_ids]
        available_trailers = Trailer.query.filter(Trailer.type == trailer_type, Trailer.id.notin_(busy_trailers)).all()
        return available_trailers

