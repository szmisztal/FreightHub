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
    """
    Handle new company creation.

    This route allows planners to create a new company by filling out the company form.
    It validates the input data and adds the new company to the database.

    Returns:
        str: Rendered HTML template for the new company form.
    """
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
    """
    Display list of all companies.

    This route fetches all companies from the database and displays them.

    Returns:
        str: Rendered HTML template displaying the list of companies.
    """
    all_companies = Company.query.all()
    if not all_companies:
        flash("Companies list is empty.", "info")
    return render_template("companies_list.html", companies=all_companies)

@planner_bp.route("/companies/<int:id>", methods=["GET"])
@login_required
@role_required("planner")
def company_details(id):
    """
    Display company details.

    This route fetches and displays details of a specific company.

    Args:
        id (int): The ID of the company.

    Returns:
        str: Rendered HTML template displaying the company details.
    """
    company = Company.query.get_or_404(id)
    return render_template("company_details.html", company=company)

@planner_bp.route("/companies/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("planner")
def edit_company(id):
    """
    Handle company data editing.

    This route allows planners to edit the data of an existing company by filling out
    the company form. It validates the input data and updates the company in the database.

    Args:
        id (int): The ID of the company to be edited.

    Returns:
        str: Rendered HTML template for the edit company form.
    """
    company = Company.query.get_or_404(id)
    form = CompanyForm(obj=company)
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
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"Edit {company} - validation error: {e}")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during {company} editing: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("company_form.html", form=form, title="Edit Company")

@planner_bp.route("/companies/confirm-delete/<int:id>", methods=["GET"])
@login_required
@role_required("planner")
def confirm_company_delete(id):
    """
    Render delete confirmation page for a company.

    This route displays a confirmation page before deleting a company.

    Args:
        id (int): The ID of the company to be deleted.

    Returns:
        str: Rendered HTML template for the delete confirmation page.
    """
    company = Company.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_company_delete.html", csrf_token=csrf_token, company=company)

@planner_bp.route("/companies/delete/<int:id>", methods=["POST"])
@login_required
@role_required("planner")
def delete_company(id):
    """
    Handle company deletion.

    This route deletes a company from the database.

    Args:
        id (int): The ID of the company to be deleted.

    Returns:
        str: Redirect to the list of companies.
    """
    try:
        company = Company.query.get_or_404(id)
        db.session.delete(company)
        db.session.commit()
        flash("Company has been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"Error during {company} deleting: {e}")
        flash(f"Error: {e}, try again", "danger")
    return redirect(url_for("planner.companies"))

@planner_bp.route("/transportation_orders/new", methods=["GET", "POST"])
@login_required
@role_required("planner")
def new_transportation_order():
    """
    Handle new transportation order creation.

    This route allows planners to create a new transportation order by filling out
    the order form. It validates the input data and adds the new order to the database.

    Returns:
        str: Rendered HTML template for the new transportation order form.
    """
    form = TransportationOrderForm()
    schema = TransportationOrderSchema()
    if request.method == "POST":
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
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"New transportation order (planner) - validation error: {e}")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during new transportation order adding: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("transportation_order_form.html", form=form, title="New Transportation Order")

@planner_bp.route("/transportation_orders", methods=["GET"])
@login_required
@role_required("planner")
def transportation_orders():
    """
    Display list of all transportation orders.

    This route fetches all incomplete transportation orders from the database and displays them.

    Returns:
        str: Rendered HTML template displaying the list of transportation orders.
    """
    all_orders = TransportationOrder.query.filter_by(completed=False).order_by(TransportationOrder.creation_date).all()
    if not all_orders:
        flash("Orders list is empty.", "info")
    return render_template("transportation_orders_list.html", orders=all_orders, title="Transportation Orders")

@planner_bp.route("/transportation_orders/<int:id>", methods=["GET"])
@login_required
@role_required("planner")
def transportation_order_details(id):
    """
    Display transportation order details.

    This route fetches and displays details of a specific transportation order.

    Args:
        id (int): The ID of the transportation order.

    Returns:
        str: Rendered HTML template displaying the transportation order details.
    """
    order = TransportationOrder.query.get_or_404(id)
    return render_template("transportation_order_details.html", order=order)

@planner_bp.route("/transportation_orders/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("planner")
def edit_transportation_order(id):
    """
    Handle transportation order editing.

    This route allows planners to edit the details of an existing transportation order
    by filling out the order form. It validates the input data and updates the order in
    the database.

    Args:
        id (int): The ID of the transportation order to be edited.

    Returns:
        str: Rendered HTML template for the edit transportation order form.
    """
    order = TransportationOrder.query.get_or_404(id)
    form = TransportationOrderForm(obj=order)
    schema = TransportationOrderSchema()
    if request.method == "POST":
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
            send_validation_errors_to_form(e, form)
            current_app.logger.exception(f"Edit {order} (planner) - validation error: {e}")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during {order} editing: {e}")
            flash(f"Error: {e}, try again", "danger")
    return render_template("transportation_order_form.html", form=form, title="Edit Transportation Order")

@planner_bp.route("/transportation_orders/confirm-delete/<int:id>", methods=["GET"])
@login_required
@role_required("planner")
def confirm_transportation_order_delete(id):
    """
    Render delete confirmation page for a transportation order.

    This route displays a confirmation page before deleting a transportation order.

    Args:
        id (int): The ID of the transportation order to be deleted.

    Returns:
        str: Rendered HTML template for the delete confirmation page.
    """
    order = TransportationOrder.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_transportation_order_delete.html", csrf_token=csrf_token, order=order)

@planner_bp.route("/transportation_orders/delete/<int:id>", methods=["POST"])
@login_required
@role_required("planner")
def delete_transportation_order(id):
    """
    Handle transportation order deletion.

    This route deletes a transportation order from the database.

    Args:
        id (int): The ID of the transportation order to be deleted.

    Returns:
        str: Redirect to the list of transportation orders.
    """
    order = TransportationOrder.query.get_or_404(id)
    try:
        db.session.delete(order)
        db.session.commit()
        flash("Transportation order has been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"Error during {order} deleting: {e}")
        flash(f"Error: {e}, try again", "danger")
    return redirect(url_for("planner.transportation_orders"))

@planner_bp.route("/transportation_orders/archived", methods=["GET"])
@login_required
@role_required("planner")
def archived_transportation_orders():
    """
    Display list of archived transportation orders.

    This route fetches all completed transportation orders from the database and displays them.

    Returns:
        str: Rendered HTML template displaying the list of archived transportation orders.
    """
    archived_orders = TransportationOrder.query.filter_by(completed=True).order_by(TransportationOrder.creation_date).all()
    if not archived_orders:
        flash("There are no archived transportation orders", "info")
    return render_template("transportation_orders_list.html", orders=archived_orders, title="Archived Transportation Orders")



