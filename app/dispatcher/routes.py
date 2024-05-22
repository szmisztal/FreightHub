from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required
from app import db
from app.common.permissions import role_required
from app.common.models import TransportationOrder
from . import dispatcher_bp
from .forms import AssignDriverForm

@dispatcher_bp.route("/orders/without-drivers", methods=["GET"])
@login_required
@role_required("dispatcher")
def orders_without_drivers():
    orders = TransportationOrder.query.filter_by(driver=None).order_by(TransportationOrder.planned_delivery_date).all()
    if not orders:
        flash("Every transportation order has assigned driver", "info")
    return render_template("transportation_orders.html", orders=orders, title="Unassigned Orders")

@dispatcher_bp.route("/orders/with-drivers", methods=["GET"])
@login_required
@role_required("dispatcher")
def orders_with_drivers():
    orders = TransportationOrder.query.filter(TransportationOrder.driver.isnot(None)).order_by(TransportationOrder.planned_delivery_date).all()
    if not orders:
        flash("None transportation order has assigned driver", "info")
    return render_template("transportation_orders.html", orders=orders, title="Assigned Orders")

@dispatcher_bp.route("/orders/assign-driver/<int:order_id>", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def assign_driver(order_id):
    order = TransportationOrder.query.get_or_404(order_id)
    form = AssignDriverForm()
    if form.validate_on_submit():
        try:
            order.driver = form.driver.data
            db.session.commit()
            flash(f"{order.assigned_driver} has been assigned to the order.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during driver to transportation order assigning: {e}")
            flash(f"Error: {e}, try again", "danger")
        return redirect(url_for("home"))
    return render_template("assign_driver_form.html", form=form, title="Assign Driver")

@dispatcher_bp.route("/orders/change-driver/<int:order_id>", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def change_assigned_driver(order_id):
    order = TransportationOrder.query.get_or_404(order_id)
    form = AssignDriverForm(obj=order)
    if form.validate_on_submit():
        try:
            if form.driver.data == "0":
                order.driver = None
            else:
                order.driver = form.driver.data
            db.session.commit()
            flash("The driver change was successful", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during transportation order`s driver editing: {e}")
            flash(f"Error: {e}, try again", "danger")
        return redirect(url_for("home"))
    return render_template("assign_driver_form.html", form=form, title="Change Driver")
