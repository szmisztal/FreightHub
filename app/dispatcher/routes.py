from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.common.permissions import role_required
from app.common.models import TransportationOrder
from . import dispatcher_bp
from .forms import AssignDriverForm

@dispatcher_bp.route("/orders/assign-driver/<int:order_id>", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def assign_driver(order_id):
    order = TransportationOrder.query.get_or_404(order_id)
    form = AssignDriverForm()
    if form.validate_on_submit():
        order.driver = form.driver.data
        db.session.commit()
        flash(f"{order.driver.first_name} {order.driver.last_name} has been assigned to the order.", "success")
        return redirect(url_for("home"))
    return render_template("assign_driver_form.html", form=form)
