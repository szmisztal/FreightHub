from flask import request, render_template, redirect, url_for, flash, current_app
from flask_wtf.csrf import generate_csrf
from flask_login import login_required, current_user
from marshmallow import ValidationError
from datetime import date
from app import db
from app.common.permissions import role_required
from app.common.models import TransportationOrder
from app.common.schemas import TransportationOrderSchema
from app.common.custom_utils import send_validation_errors_to_form
from . import planner_bp
from .models import Company
from .forms import CompanyForm, TransportationOrderForm
from .schemas import CompanySchema

@planner_bp.route("/companies/new", methods=["GET", "POST"])
@login_required
@role_required("planner")
def new_company():
    form = CompanyForm()
    schema = CompanySchema()
    if request.method == "POST":
        company_data = {
            "company_name": form.company_name.data,
            "country": form.country.data,
            "town": form.town.data,
            "postal_code": form.postal_code.data,
            "street": form.street.data,
            "street_number": form.street_number.data,
            "phone_number": form.phone_number.data
        }
        try:
            result = schema.load(company_data)
            company = Company(**result)
            db.session.add(company)
            db.session.commit()
            flash("New company has been added.", "success")
            return redirect(url_for("home"))
        except ValidationError as e:
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"New company - validation error: {e}")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during new company adding: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("company_form.html", form=form, title="New Company")

@planner_bp.route("/companies", methods=["GET"])
@login_required
@role_required("planner")
def companies():
    all_companies = Company.query.all()
    if not all_companies:
        flash("Companies list is empty.", "info")
    return render_template("companies_list.html", companies=all_companies)


@planner_bp.route("/companies/<int:id>", methods=["GET"])
@login_required
@role_required("planner")
def company_details(id):
    company = Company.query.get_or_404(id)
    return render_template("company_details.html", company=company)

@planner_bp.route("/companies/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("planner")
def edit_company(id):
    company = Company.query.get_or_404(id)
    form = CompanyForm(obj=company)
    schema = CompanySchema()
    if form.validate_on_submit():
        company_data = {
            "company_name": form.company_name.data,
            "country": form.country.data,
            "town": form.town.data,
            "postal_code": form.postal_code.data,
            "street": form.street.data,
            "street_number": form.street_number.data,
            "phone_number": form.phone_number.data
        }
        try:
            result = schema.load(company_data)
            company.company_name = result["company_name"]
            company.country = result["country"]
            company.town = result["town"]
            company.postal_code = result["postal_code"]
            company.street = result["street"]
            company.street_number = result["street_number"]
            company.phone_number = result["phone_number"]
            db.session.commit()
            flash("Company details updated successfully.", "success")
            return redirect(url_for("planner.companies"))
        except ValidationError as e:
            current_app.logger.exception(f"Edit company - validation error: {e}")
            flash(f"Validation error: {e}", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during company editing: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("company_form.html", form=form, title="Edit Company")

@planner_bp.route("/companies/confirm-delete/<int:id>", methods=["GET"])
@login_required
@role_required("planner")
def confirm_company_delete(id):
    company = Company.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_company_delete.html", csrf_token=csrf_token, company=company)

@planner_bp.route("/companies/delete/<int:id>", methods=["POST"])
@login_required
@role_required("planner")
def delete_company(id):
    try:
        company = Company.query.get_or_404(id)
        db.session.delete(company)
        db.session.commit()
        flash("Company has been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"Error during company deleting: {e}")
        flash(f"Error: {e}, try again", "danger")
    return redirect(url_for("planner.companies"))

@planner_bp.route("/transportation_orders/new", methods=["GET", "POST"])
@login_required
@role_required("planner")
def new_transportation_order():
    form = TransportationOrderForm()
    schema = TransportationOrderSchema()
    if form.validate_on_submit():
        transportation_order_data = {
            "creation_date": str(date.today()),
            "created_by": current_user.id,
            "planned_delivery_date": str(form.planned_delivery_date.data),
            "trailer_type": form.trailer_type.data,
            "load_weight": form.load_weight.data,
            "loading_place": form.loading_place.data,
            "delivery_place": form.delivery_place.data
        }
        try:
            result = schema.load(transportation_order_data)
            order = TransportationOrder(**result)
            db.session.add(order)
            db.session.commit()
            flash("New transportation order has been created.", "success")
            return redirect(url_for("home"))
        except ValidationError as e:
            current_app.logger.exception(f"New transportation order (planner) - validation error: {e}")
            flash(f"Validation error: {e}", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during new transportation order adding: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("transportation_order_form.html", form=form, title="New Transportation Order")

@planner_bp.route("/transportation_orders", methods=["GET"])
@login_required
@role_required("planner")
def transportation_orders():
    all_orders = TransportationOrder.query.filter_by(completed=False).order_by(TransportationOrder.creation_date).all()
    if not all_orders:
        flash("Orders list is empty.", "info")
    return render_template("transportation_orders_list.html", orders=all_orders, title="Transportation Orders")

@planner_bp.route("/transportation_orders/<int:id>", methods=["GET"])
@login_required
@role_required("planner")
def transportation_order_details(id):
    order = TransportationOrder.query.get_or_404(id)
    return render_template("transportation_order_details.html", order=order)

@planner_bp.route("/transportation_orders/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("planner")
def edit_transportation_order(id):
    order = TransportationOrder.query.get_or_404(id)
    form = TransportationOrderForm(obj=order)
    schema = TransportationOrderSchema()
    if form.validate_on_submit():
        transportation_order_data = {
            "creation_date": str(order.creation_date),
            "created_by": current_user.id,
            "planned_delivery_date": str(form.planned_delivery_date.data),
            "trailer_type": form.trailer_type.data,
            "load_weight": form.load_weight.data,
            "loading_place": form.loading_place.data,
            "delivery_place": form.delivery_place.data
        }
        try:
            result = schema.load(transportation_order_data)
            order.planned_delivery_date = result["planned_delivery_date"]
            order.trailer_type = result["trailer_type"]
            order.load_weight = result["load_weight"]
            order.loading_place = result["loading_place"]
            order.delivery_place = result["delivery_place"]
            db.session.commit()
            flash("Transportation order details updated successfully.", "success")
            return redirect(url_for("planner.transportation_orders"))
        except ValidationError as e:
            current_app.logger.exception(f"Edit transportation order (planner) - validation error: {e}")
            flash(f"Validation error: {e}", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during transportation order editing: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("transportation_order_form.html", form=form, title="Edit Transportation Order")

@planner_bp.route("/transportation_orders/confirm-delete/<int:id>", methods=["GET"])
@login_required
@role_required("planner")
def confirm_transportation_order_delete(id):
    order = TransportationOrder.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_transportation_order_delete.html", csrf_token=csrf_token, order=order)

@planner_bp.route("/transportation_orders/delete/<int:id>", methods=["POST"])
@login_required
@role_required("planner")
def delete_transportation_order(id):
    order = TransportationOrder.query.get_or_404(id)
    try:
        db.session.delete(order)
        db.session.commit()
        flash("Transportation order has been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"Error during transportation order deleting: {e}")
        flash(f"Error: {e}, try again", "danger")
    return redirect(url_for("planner.transportation_orders"))

@planner_bp.route("/transportation_orders/archived", methods=["GET"])
@login_required
@role_required("planner")
def archived_transportation_orders():
    archived_orders = TransportationOrder.query.filter_by(completed=True).order_by(TransportationOrder.creation_date).all()
    if not archived_orders:
        flash("There are any archived transportation orders", "info")
    return render_template("transportation_orders_list.html", orders=archived_orders, title="Archived Transportation Orders")


