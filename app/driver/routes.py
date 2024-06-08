from flask import render_template, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from flask_wtf.csrf import generate_csrf
from app import db
from app.common.permissions import role_required
from app.common.models import TransportationOrder
from . import driver_bp

@driver_bp.route("/current-order", methods=["GET"])
@login_required
@role_required("driver")
def current_transportation_order():
    """
    Display the current transportation order for the logged-in driver.

    This route fetches the current transportation order assigned to the driver
    and displays it. If no current order is found, a flash message is shown
    and the user is redirected to the home page.

    Returns:
        str: Rendered HTML template for the current order page.
    """
    order = TransportationOrder.query.filter_by(driver=current_user.id, completed=False).first()
    if not order:
        flash("You don’t have any orders right now", "info")
        return redirect(url_for("home"))
    return render_template("current_order.html", order=order)

@driver_bp.route("/confirm-finish-order/<int:id>", methods=["GET"])
@login_required
@role_required("driver")
def confirm_finish_order(id):
    """
    Display confirmation page for finishing a transportation order.

    This route displays a confirmation page for the driver to confirm
    the completion of a transportation order.

    Args:
        id (int): The ID of the transportation order to be finished.

    Returns:
        str: Rendered HTML template for the finish order confirmation page.
    """
    current_order = TransportationOrder.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_finish_order.html", csrf_token=csrf_token, current_order=current_order)

@driver_bp.route("/finish/<int:id>", methods=["POST"])
@login_required
@role_required("driver")
def finish_order(id):
    """
    Mark a transportation order as completed.

    This route marks the specified transportation order as completed
    and updates the database. If an error occurs, a flash message is shown
    and the user is redirected to the home page.

    Args:
        id (int): The ID of the transportation order to be completed.

    Returns:
        str: Redirect to the home page.
    """
    try:
        current_order = TransportationOrder.query.get_or_404(id)
        current_order.completed = True
        db.session.commit()
        flash("Transportation order has been completed.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"Error during {current_order} finishing by driver "
                                     f"{current_user.first_name} {current_user.last_name}: {e}")
        flash(f"Error: {e}, try again", "danger")
    return redirect(url_for("home"))

@driver_bp.route("/archived-orders", methods=["GET"])
@login_required
@role_required("driver")
def completed_orders():
    """
    Display list of archived transportation orders for the logged-in driver.

    This route fetches and displays all completed transportation orders assigned
    to the driver.

    Returns:
        str: Rendered HTML template displaying the list of archived orders.
    """
    archived_orders = TransportationOrder.query.filter_by(driver=current_user.id, completed=True).order_by(TransportationOrder.planned_delivery_date).all()
    if not archived_orders:
        flash("You don’t have any archived orders", "info")
        return redirect(url_for("home"))
    return render_template("archived_orders.html", archived_orders=archived_orders)

