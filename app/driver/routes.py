from flask import render_template, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from flask_wtf.csrf import generate_csrf
from app import db
from app.common.permissions import role_required
from app.common.models import TransportationOrder
from . import driver_bp

@driver_bp.route("/orders/current-order", methods=["GET"])
@login_required
@role_required("driver")
def current_transportation_order():
    current_order = TransportationOrder.query.filter_by(driver=current_user.id).first()
    if not current_order:
        flash("You don’t have any orders right now", "info")
        return redirect(url_for("home"))
    return render_template("current_order.html", current_order=current_order)

@driver_bp.route("/orders/confirm-finish-order/<int:id>", methods=["GET"])
@login_required
@role_required("driver")
def confirm_finish_order(id):
    current_order = TransportationOrder.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_finish_order.html", csrf_token=csrf_token, current_order=current_order)

@driver_bp.route("/orders/finish/<int:id>", methods=["POST"])
@login_required
@role_required("driver")
def finish_order(id):
    try:
        current_order = TransportationOrder.query.get_or_404(id)
        current_order.completed = True
        db.session.commit()
        flash("Transportation order has been completed.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"Error during transportation order finishing by driver "
                                     f"{current_user.first_name} {current_user.last_name}: {e}")
        flash(f"Error: {e}, try again", "danger")
    return redirect(url_for("home"))

@driver_bp.route("/orders/archived", methods=["GET"])
@login_required
@role_required("driver")
def completed_orders():
    archived_orders = TransportationOrder.query.filter_by(driver=current_user.id, completed=True).order_by(TransportationOrder.date).all()
    if not archived_orders:
        flash("You don’t have any archived orders", "info")
        return redirect(url_for("home"))
    return render_template("archived_orders.html", archived_orders=archived_orders)
