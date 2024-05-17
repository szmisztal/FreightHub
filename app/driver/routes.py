from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from flask_wtf.csrf import generate_csrf
from app import db
from app.planner.models import TransportationOrder
from . import driver_bp

@driver_bp.route("/orders/current_order", methods=["GET"])
def current_transportation_order():
    current_order = TransportationOrder.query.filter_by(driver=current_user.id).first()
    if current_order:
        return render_template("current_order.html", current_order=current_order)
    else:
        flash("You don’t have any orders right now", "info")
        return redirect(url_for("home"))

@driver_bp.route("/orders/confirm-finish-order/<int:id>", methods=["GET"])
def confirm_finish_order(id):
    current_order = TransportationOrder.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_finish_order.html", csrf_token=csrf_token, current_order=current_order)

@driver_bp.route("/orders/finish/<int:id>", methods=["POST"])
def finish_order(id):
    current_order = TransportationOrder.query.get_or_404(id)
    current_order.completed = True
    db.session.commit()
    flash("Transportation order has been completed.", "success")
    return redirect(url_for("home"))
