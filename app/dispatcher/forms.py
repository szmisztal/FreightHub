from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, IntegerField
from wtforms.validators import Optional
from app import db
from app.common.models import User, TransportationOrder, Trailer
from .models import TractorHead

class TractorHeadForm(FlaskForm):
    """
    Form for adding or updating a tractor head.

    This form collects information about the tractor head including brand and
    registration number.
    """
    brand = StringField("Brand")
    registration_number = StringField("Registration Number")
    submit = SubmitField("Submit")

class TrailerForm(FlaskForm):
    """
    Form for adding or updating a trailer.

    This form collects information about the trailer including type, maximum load capacity and
    registration number.
    """
    type = SelectField("Type", choices=[
        # ("Tanker", "Tanker trailer"),
        ("Curtain side", "Curtain-side trailer"),
        ("Refrigerated", "Refrigerated trailer"),
        ("Tipper", "Tipper trailer"),
        ("Low loader", "Low-loader trailer"),
        ("Container", "Container trailer"),
        ("Self-unloading", "Self-unloading trailer"),
        ("Insulated", "Insulated trailer")
    ])
    max_load_capacity = IntegerField("Maximum Load Capacity")
    registration_number = StringField("Registration Number")
    # chambers_number = IntegerField("Chambers number", [Optional()])
    submit = SubmitField("Submit")

class CompletingTheTransportationOrderForm(FlaskForm):
    """
    Form for completing the details of a transportation order.

    This form allows dispatchers to assign a driver, tractor head, and trailer
    to a transportation order.
    """
    driver = SelectField("Driver", choices=[])
    tractor_head = SelectField("Tractor Head", choices=[])
    trailer = SelectField("Trailer", choices=[])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with choices for drivers, tractor heads, and trailers.

        This method populates the select fields with available options, including
        the currently assigned options if any.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(CompletingTheTransportationOrderForm, self).__init__(*args, **kwargs)

        assigned_driver = kwargs.get("obj").assigned_driver
        assigned_tractor_head = kwargs.get("obj").assigned_tractor_head
        assigned_trailer = kwargs.get("obj").assigned_trailer

        driver_choices = [(0, "No Driver")]
        if assigned_driver:
            driver_choices.append((assigned_driver.id, f"{assigned_driver.first_name} {assigned_driver.last_name}"))
        driver_choices += [(driver.id, f"{driver.first_name} {driver.last_name}") for driver in self.get_available_drivers()]
        self.driver.choices = driver_choices

        tractor_head_choices = [(0, "No Tractor Head")]
        if assigned_tractor_head:
            tractor_head_choices.append((assigned_tractor_head.id, f"{assigned_tractor_head.brand} {assigned_tractor_head.registration_number}"))
        tractor_head_choices += [(tractor.id, f"{tractor.brand} {tractor.registration_number}") for tractor in self.get_available_tractor_heads()]
        self.tractor_head.choices = tractor_head_choices

        trailer_choices = [(0, "No Trailer")]
        if assigned_trailer:
            trailer_choices.append((assigned_trailer.id, f"{assigned_trailer.registration_number}"))
        trailer_choices += [(trailer.id, f"{trailer.registration_number}") for trailer in self.get_available_trailer(
            kwargs.get("obj").trailer_type,
            kwargs.get("obj").load_weight
        )]
        self.trailer.choices = trailer_choices

    def get_available_drivers(self):
        """
        Get a list of available drivers.

        This method queries the database to find drivers who are not currently
        assigned to an active transportation order.

        Returns:
            list: A list of available drivers.
        """
        all_drivers = User.query.filter(User.role == "driver").all()
        busy_driver_ids = db.session.query(TransportationOrder.driver).filter(
            TransportationOrder.completed == False,
            TransportationOrder.driver.isnot(None)
        ).all()
        busy_driver_ids = [driver_id for (driver_id,) in busy_driver_ids]
        available_drivers = [driver for driver in all_drivers if driver.id not in busy_driver_ids]
        return available_drivers

    def get_available_tractor_heads(self):
        """
        Get a list of available tractor heads.

        This method queries the database to find tractor heads that are not
        currently assigned to an active transportation order.

        Returns:
            list: A list of available tractor heads.
        """
        all_tractor_heads = TractorHead.query.all()
        busy_tractor_head_ids = db.session.query(TransportationOrder.tractor_head).filter(
            TransportationOrder.completed == False,
            TransportationOrder.tractor_head.isnot(None)
        ).all()
        busy_tractor_head_ids = [tractor_head_id for (tractor_head_id,) in busy_tractor_head_ids]
        available_tractor_heads = [tractor_head for tractor_head in all_tractor_heads if tractor_head.id not in busy_tractor_head_ids]
        return available_tractor_heads

    def get_available_trailer(self, trailer_type, order_load_weight):
        """
        Get a list of available trailers of a specific type.

        This method queries the database to find trailers of the specified type
        that are not currently assigned to an active transportation order.

        Args:
            trailer_type (str): The type of the trailer.

        Returns:
            list: A list of available trailers of the specified type.
        """
        busy_trailer_ids = db.session.query(TransportationOrder.trailer).filter(
            TransportationOrder.completed == False,
            TransportationOrder.trailer.isnot(None)
        ).all()
        busy_trailers = [trailer_id for (trailer_id,) in busy_trailer_ids]
        available_trailers = Trailer.query.filter(
            Trailer.type == trailer_type,
            Trailer.max_load_capacity >= order_load_weight,
            Trailer.id.notin_(busy_trailers)
        ).all()
        return available_trailers


