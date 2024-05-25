from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required
from flask_wtf.csrf import generate_csrf
from app import db
from app.common.permissions import role_required
from app.common.models import TransportationOrder
from . import dispatcher_bp
from .forms import AssignDriverForm, TractorHeadForm, TrailerForm
from .models import TractorHead, Trailer

@dispatcher_bp.route("/tractor_heads/new", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def new_tractor_head():
    form = TractorHeadForm()
    if form.validate_on_submit():
        try:
            tractor_head = create_tractor_head(form)
            db.session.add(tractor_head)
            db.session.commit()
            flash("New tractor head has been added", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during new tractor head adding: {e}")
            flash(f"Error: {e}, try again", "danger")
        return redirect(url_for("home"))
    return render_template("tractor_head_form.html", form=form, title="New Tractor Head")

def create_tractor_head(form):
    return TractorHead(
        brand=form.brand.data,
        registration_number=form.registration_number.data
    )

@dispatcher_bp.route("/tractor_heads", methods=["GET"])
@login_required
@role_required("dispatcher")
def tractor_heads():
    all_tractor_heads = TractorHead.query.all()
    if not all_tractor_heads:
        flash("Tractor heads list is empty.", "info")
    return render_template("tractor_heads_list.html", tractor_heads=tractor_heads)

@dispatcher_bp.route("/tractor_heads/<int:id>", methods=["GET"])
@login_required
@role_required("dispatcher")
def tractor_head_details(id):
    tractor_head = TractorHead.query.get_or_404(id)
    return render_template("tractor_head_details.html", tractor_head=tractor_head)

@dispatcher_bp.route("/tractor_heads/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def edit_tractor_head(id):
    tractor_head = TractorHead.query.get_or_404(id)
    form = TractorHead(obj=tractor_head)
    if form.validate_on_submit():
        try:
            tractor_head.brand = form.brand.data
            tractor_head.registration_number = form.registration_number.data
            db.session.commit()
            flash("Tractor head details updated successfully.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during tractor head editing: {e}")
            flash(f"Error: {e}, try again", "danger")
        return redirect(url_for("dispatcher.tractor_heads"))
    return render_template("tractor_head_form.html", form=form, title="Edit Tractor Head")

@dispatcher_bp.route("/tractor_heads/confirm-delete/<int:id>", methods=["GET"])
@login_required
@role_required("dispatcher")
def confirm_tractor_head_delete(id):
    tractor_head = TractorHead.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_tractor_head_delete.html", csrf_token=csrf_token, tractor_head=tractor_head)

@dispatcher_bp.route("/tractor_heads/delete/<int:id>", methods=["POST"])
@login_required
@role_required("dispatcher")
def delete_tractor_head(id):
    try:
        tractor_head = TractorHead.query.get_or_404(id)
        db.session.delete(tractor_head)
        db.session.commit()
        flash("Tractor head has been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"Error during tractor head deleting: {e}")
        flash(f"Error: {e}, try again", "danger")
    return redirect(url_for("dispatcher.tractor_heads"))

@dispatcher_bp.route("/trailers/new", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def new_trailer():
    form = TrailerForm()
    if form.validate_on_submit():
        try:
            trailer = create_trailer(form)
            db.session.add(trailer)
            db.session.commit()
            flash("New trailer has been added", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during new trailer adding: {e}")
            flash(f"Error: {e}, try again", "danger")
        return redirect(url_for("home"))
    return render_template("trailer_form.html", form=form, title="New Trailer")

def create_trailer(form):
    return Trailer(
        type=form.type.data,
        registration_number=form.registration_number.data
    )

@dispatcher_bp.route("/trailers", methods=["GET"])
@login_required
@role_required("dispatcher")
def trailers():
    all_trailers = Trailer.query.all()
    if not all_trailers:
        flash("Trailers list is empty.", "info")
    return render_template("trailers_list.html", trailers=trailers)

@dispatcher_bp.route("/trailers/<int:id>", methods=["GET"])
@login_required
@role_required("dispatcher")
def trailer_details(id):
    trailer = Trailer.query.get_or_404(id)
    return render_template("trailer_details.html", trailer=trailer)

@dispatcher_bp.route("/trailers/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def edit_trailer(id):
    trailer = Trailer.query.get_or_404(id)
    form = Trailer(obj=trailer)
    if form.validate_on_submit():
        try:
            trailer.type = form.type.data
            trailer.registration_number = form.registration_number.data
            db.session.commit()
            flash("Trailer details updated successfully.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during trailer editing: {e}")
            flash(f"Error: {e}, try again", "danger")
        return redirect(url_for("dispatcher.trailers"))
    return render_template("trailer_form.html", form=form, title="Edit Trailer")

@dispatcher_bp.route("/trailers/confirm-delete/<int:id>", methods=["GET"])
@login_required
@role_required("dispatcher")
def confirm_trailer_delete(id):
    trailer = Trailer.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_trailer_delete.html", csrf_token=csrf_token, trailer=trailer)

@dispatcher_bp.route("/trailers/delete/<int:id>", methods=["POST"])
@login_required
@role_required("dispatcher")
def delete_trailer(id):
    try:
        trailer = Trailer.query.get_or_404(id)
        db.session.delete(trailer)
        db.session.commit()
        flash("Trailerd has been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"Error during trailer deleting: {e}")
        flash(f"Error: {e}, try again", "danger")
    return redirect(url_for("dispatcher.trailers"))

@dispatcher_bp.route("/orders/without-drivers", methods=["GET"])
@login_required
@role_required("dispatcher")
def orders_without_drivers():
    orders = TransportationOrder.query.filter_by(driver=None, completed=False).order_by(TransportationOrder.planned_delivery_date).all()
    if not orders:
        flash("Every transportation order has assigned driver", "info")
    return render_template("transportation_orders.html", orders=orders, title="Unassigned Orders")

@dispatcher_bp.route("/orders/with-drivers", methods=["GET"])
@login_required
@role_required("dispatcher")
def orders_with_drivers():
    orders = TransportationOrder.query.filter(TransportationOrder.driver.isnot(None)).filter_by(completed=False).order_by(TransportationOrder.planned_delivery_date).all()
    if not orders:
        flash("None transportation order has assigned driver", "info")
    return render_template("transportation_orders.html", orders=orders, title="Assigned Orders")

@dispatcher_bp.route("/orders/assign-driver/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def assign_driver(id):
    order = TransportationOrder.query.get_or_404(id)
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

@dispatcher_bp.route("/orders/change-driver/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def change_assigned_driver(id):
    order = TransportationOrder.query.get_or_404(id)
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
