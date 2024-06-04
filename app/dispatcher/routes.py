from flask import request, render_template, redirect, url_for, flash, current_app
from flask_login import login_required
from flask_wtf.csrf import generate_csrf
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from app import db
from app.common.permissions import role_required
from app.common.models import TransportationOrder, Trailer
from app.common.schemas import TransportationOrderSchema
from app.common.custom_utils import send_validation_errors_to_form
from . import dispatcher_bp
from .forms import CompletingTheTransportationOrderForm, TractorHeadForm, TrailerForm
from .models import TractorHead
from .schemas import TractorHeadSchema, TrailerSchema

@dispatcher_bp.route("/tractor_heads/new", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def new_tractor_head():
    form = TractorHeadForm()
    schema = TractorHeadSchema()
    if request.method == "POST":
        tractor_head_data = {
            "brand": form.brand.data,
            "registration_number": form.registration_number.data.upper()
        }
        try:
            result = schema.load(tractor_head_data)
            tractor_head = TractorHead(**result)
            db.session.add(tractor_head)
            db.session.commit()
            flash("New tractor head has been added", "success")
            return redirect(url_for("home"))
        except ValidationError as e:
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"New tractor head - validation error: {e}")
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.exception(f"Adding new tractor head error: {e}")
            flash("Registration number is already in use, choose another.", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during new tractor head adding: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("tractor_head_form.html", form=form, title="New Tractor Head")

@dispatcher_bp.route("/tractor_heads", methods=["GET"])
@login_required
@role_required("dispatcher")
def tractor_heads():
    all_tractor_heads = TractorHead.query.all()
    if not all_tractor_heads:
        flash("Tractor heads list is empty.", "info")
    return render_template("tractor_heads_list.html", tractor_heads=all_tractor_heads)

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
    form = TractorHeadForm(obj=tractor_head)
    schema = TractorHeadSchema()
    if request.method == "POST":
        tractor_head_data = {
            "brand": form.brand.data,
            "registration_number": form.registration_number.data
        }
        try:
            result = schema.load(tractor_head_data)
            tractor_head.brand = result["brand"]
            tractor_head.registration_number = result["registration_number"]
            db.session.commit()
            flash("Tractor head details updated successfully.", "success")
            return redirect(url_for("dispatcher.tractor_heads"))
        except ValidationError as e:
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"Edit {tractor_head} - validation error: {e}")
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.exception(f"Editing {tractor_head} error: {e}")
            flash("Registration number is already in use, choose another.", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during {tractor_head} editing: {e}")
            flash(f"Error: {e}, try again", "danger")
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
        current_app.logger.exception(f"Error during {tractor_head} deleting: {e}")
        flash(f"Error: {e}, try again", "danger")
    return redirect(url_for("dispatcher.tractor_heads"))

@dispatcher_bp.route("/trailers/new", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def new_trailer():
    form = TrailerForm()
    schema = TrailerSchema()
    if request.method == "POST":
        trailer_data = {
            "type": form.type.data,
            "registration_number": form.registration_number.data.upper()
        }
        try:
            result = schema.load(trailer_data)
            trailer = Trailer(**result)
            db.session.add(trailer)
            db.session.commit()
            flash("New trailer has been added", "success")
            return redirect(url_for("home"))
        except ValidationError as e:
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"New trailer - validation error: {e}")
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.exception(f"Adding new trailer error: {e}")
            flash("Registration number is already in use, choose another.", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during new trailer adding: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("trailer_form.html", form=form, title="New Trailer")

@dispatcher_bp.route("/trailers", methods=["GET"])
@login_required
@role_required("dispatcher")
def trailers():
    all_trailers = Trailer.query.all()
    if not all_trailers:
        flash("Trailers list is empty.", "info")
    return render_template("trailers_list.html", trailers=all_trailers)

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
    form = TrailerForm(obj=trailer)
    schema = TrailerSchema()
    if request.method == "POST":
        trailer_data = {
            "type": form.type.data,
            "registration_number": form.registration_number.data
        }
        try:
            result = schema.load(trailer_data)
            trailer.type = result["type"]
            trailer.registration_number = result["registration_number"].upper()
            db.session.commit()
            flash("Trailer details updated successfully.", "success")
            return redirect(url_for("dispatcher.trailers"))
        except ValidationError as e:
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"Edit {trailer} - validation error: {e}")
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.exception(f"Editing {trailer} error: {e}")
            flash("Registration number is already in use, choose another.", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during {trailer} editing: {e}")
            flash(f"Error: {e}, try again", "danger")
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
        current_app.logger.exception(f"Error during {trailer} deleting: {e}")
        flash(f"Error: {e}, try again", "danger")
    return redirect(url_for("dispatcher.trailers"))

@dispatcher_bp.route("/orders/active", methods=["GET"])
@login_required
@role_required("dispatcher")
def active_transport_orders():
    orders = TransportationOrder.query.filter_by(completed=False).order_by(TransportationOrder.planned_delivery_date).all()
    if not orders:
        flash("There are no orders yet", "info")
    return render_template("transportation_orders.html", orders=orders)

@dispatcher_bp.route("/orders/complete/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("dispatcher")
def complete_the_order(id):
    order = TransportationOrder.query.get_or_404(id)
    form = CompletingTheTransportationOrderForm(obj=order)
    schema = TransportationOrderSchema()
    if request.method == "POST":
        transportation_order_data = {
            "creation_date": str(order.creation_date),
            "created_by": order.created_by,
            "planned_delivery_date": str(order.planned_delivery_date),
            "trailer_type": order.trailer_type,
            "tractor_head": form.tractor_head.data,
            "trailer": form.trailer.data,
            "load_weight": order.load_weight,
            "loading_place": order.loading_place,
            "delivery_place": order.delivery_place,
            "driver": form.driver.data,
            "completed": order.completed
        }
        try:
            result = schema.load(transportation_order_data)
            order.driver = result["driver"] if form.driver.data != "0" else None
            order.tractor_head = result["tractor_head"] if form.tractor_head.data != "0" else None
            order.trailer = result["trailer"] if form.trailer.data != "0" else None
            db.session.commit()
            flash("Successfully completed the order", "success")
            return redirect(url_for("dispatcher.active_transport_orders"))
        except ValidationError as e:
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"Edit {order} (dispatcher) - validation error: {e}")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during completing the {order}: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("completing_the_order_form.html", form=form)

