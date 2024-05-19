from flask import render_template, redirect, url_for, flash
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
    orders = TransportationOrder.query.filter_by(driver=None).order_by(TransportationOrder.date).all()
    if not orders:
        flash("Every transportation order has assigned driver", "info")
        return redirect(url_for("home"))
    return render_template("transportation_orders_list.html", orders=orders, title="Unassigned Orders")

@dispatcher_bp.route("/orders/with-drivers", methods=["GET"])
@login_required
@role_required("dispatcher")
def orders_with_drivers():
    orders = TransportationOrder.query.filter(TransportationOrder.driver.isnot(None)).order_by(TransportationOrder.date).all()
    if not orders:
        flash("None transportation order has assigned driver", "info")
        return redirect(url_for("home"))
    return render_template("transportation_orders_list.html", orders=orders, title="Assigned Orders")

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
    return render_template("assign_driver_form.html", form=form, title="Assign Driver")

@dispatcher_bp.route("/orders/change-driver/<int:order_id>", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def change_assigned_driver(order_id):
    order = TransportationOrder.query.get_or_404(order_id)
    form = AssignDriverForm(obj=order)
    if form.validate_on_submit():
        order.driver = form.driver.data
        db.session.commit()
        flash("The driver change was successful", "success")
        return redirect(url_for("home"))
    return render_template("assign_driver_form.html", form=form, title="Change Driver")
