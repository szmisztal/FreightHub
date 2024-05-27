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
            tractor_head_choices.append((assigned_tractor_head.id, f"{assigned_tractor_head.registration_number}"))
        tractor_head_choices += [(t.id, f"{t.registration_number}") for t in self.get_available_tractor_heads()]
        self.tractor_head.choices = tractor_head_choices

        trailer_choices = [(0, "No Trailer")]
        if assigned_trailer:
            trailer_choices.append((assigned_trailer.id, f"{assigned_trailer.registration_number}"))
        trailer_choices += [(tr.id, f"{tr.registration_number}") for tr in self.get_available_trailer(kwargs.get("obj").trailer_type)]
        self.trailer.choices = trailer_choices

    def get_available_drivers(self):
        active_driver_ids = db.session.query(TransportationOrder.driver).filter(
            TransportationOrder.completed == False,
            TransportationOrder.driver.isnot(None)
        ).distinct().subquery()
        available_drivers = User.query.filter(User.role == "driver", User.id.notin_(active_driver_ids)).all()
        return available_drivers

    def get_available_tractor_heads(self):
        active_tractor_heads_ids = db.session.query(TransportationOrder.tractor_head).filter(
            TransportationOrder.completed == False,
            TransportationOrder.tractor_head.isnot(None)
        ).distinct().subquery()
        available_tractor_heads = TractorHead.query.filter(TractorHead.id.notin_(active_tractor_heads_ids)).all()
        return available_tractor_heads

    def get_available_trailer(self, trailer_type):
        active_trailers_ids = db.session.query(TransportationOrder.trailer).filter(
            TransportationOrder.completed == False,
            TransportationOrder.trailer.isnot(None)
        ).distinct().subquery()
        available_trailer = Trailer.query.filter(Trailer.type == trailer_type, Trailer.id.notin_(active_trailers_ids)).all()
        return available_trailer

