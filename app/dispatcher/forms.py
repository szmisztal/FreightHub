from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from app import db
from app.common.models import User, TransportationOrder

class AssignDriverForm(FlaskForm):
    driver = SelectField("Driver", choices=[])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(AssignDriverForm, self).__init__(*args, **kwargs)
        self.driver.choices = [(u.id, f"{u.first_name} {u.last_name}") for u in self.get_available_drivers()]

    def get_available_drivers(self):
        assigned_driver_ids = db.session.query(TransportationOrder.driver).filter(TransportationOrder.driver.isnot(None)).distinct()
        available_drivers = User.query.filter(User.role == "driver", User.id.notin_(assigned_driver_ids)).all()
        return available_drivers
