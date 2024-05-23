from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from app import db
from app.common.models import User, TransportationOrder

class AssignDriverForm(FlaskForm):
    driver = SelectField("Driver", choices=[], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(AssignDriverForm, self).__init__(*args, **kwargs)
        self.driver.choices = [(0, "No Driver")] + [(u.id, f"{u.first_name} {u.last_name}") for u in self.get_available_drivers()]

    def get_available_drivers(self):
        active_driver_ids = db.session.query(TransportationOrder.driver).filter(
            TransportationOrder.completed == False,
            TransportationOrder.driver.isnot(None)
        ).distinct().subquery()

        available_drivers = User.query.filter(
            User.role == "driver",
            User.id.notin_(active_driver_ids)
        ).all()
        
        return available_drivers
