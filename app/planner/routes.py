from flask import render_template, redirect, url_for, flash, current_app
from flask_wtf.csrf import generate_csrf
from flask_login import login_required, current_user
from app import db
from app.common.permissions import role_required
from app.common.models import TransportationOrder
from . import planner_bp
from .models import Company
from .forms import CompanyForm, TransportationOrderForm

@planner_bp.route("/companies/new", methods=["GET", "POST"])
@login_required
@role_required("planner")
def new_company():
    form = CompanyForm()
    if form.validate_on_submit():
        try:
            company = create_company(form)
            db.session.add(company)
            db.session.commit()
            flash("New company has been added.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during new company adding: {e}")
            flash(f"Error: {e}, try again", "danger")
        return redirect(url_for("home"))
    return render_template("company_form.html", form=form, title="New Company")

def create_company(form):
    return Company(
        company_name=form.company_name.data,
        country=form.country.data,
        town=form.town.data,
        postal_code=form.postal_code.data,
        street=form.street.data,
        street_number=form.street_number.data,
        phone_number=form.phone_number.data
    )

@planner_bp.route("/companies", methods=["GET"])
@login_required
@role_required("planner")
def companies():
    all_companies = Company.query.all()
    if not all_companies:
        flash("Companies list is empty.", "info")
        return render_template("companies_list.html", companies=all_companies)
    return render_template("companies_list.html", companies=all_companies)


@planner_bp.route("/companies/<int:company_id>", methods=["GET"])
@login_required
@role_required("planner")
def company_details(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template("company_details.html", company=company)

@planner_bp.route("/companies/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("planner")
def edit_company(id):
    company = Company.query.get_or_404(id)
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        try:
            company.name = form.company_name.data
            company.country = form.country.data
            company.town = form.town.data
            company.postal_code = form.postal_code.data
            company.street = form.street.data
            company.street_number = form.street_number.data
            company.phone_number = form.phone_number.data
            db.session.commit()
            flash("Company details updated successfully.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during company editing: {e}")
            flash(f"Error: {e}, try again", "danger")
        return redirect(url_for("companies"))
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
    return redirect(url_for("companies"))

@planner_bp.route("/orders/new", methods=["GET", "POST"])
@login_required
@role_required("planner")
def new_transportation_order():
    form = TransportationOrderForm()
    if form.validate_on_submit():
        try:
            order = create_order(form)
            db.session.add(order)
            db.session.commit()
            flash("New transportation order has been created.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during new transportation order adding: {e}")
            flash(f"Error: {e}, try again", "danger")
        return redirect(url_for("home"))
    return render_template("transportation_order_form.html", form=form, title="New Transportation Order")

def create_order(form):
    return TransportationOrder(
        created_by=current_user.id,
        planned_delivery_date=form.planned_delivery_date.data,
        trailer_type=form.trailer_type.data,
        load_weight=form.load_weight.data,
        loading_place=form.loading_place.data,
        delivery_place=form.delivery_place.data
    )

@planner_bp.route("/orders", methods=["GET"])
@login_required
@role_required("planner")
def transportation_orders():
    all_orders = TransportationOrder.query.all()
    if not all_orders:
        flash("Orders list is empty.", "info")
        return render_template("transportation_orders_list.html", orders=all_orders)
    return render_template("transportation_orders_list.html", orders=all_orders)

@planner_bp.route("/orders/<int:order_id>", methods=["GET"])
@login_required
@role_required("planner")
def transportation_order_details(order_id):
    order = TransportationOrder.query.get_or_404(order_id)
    return render_template("transportation_order_details.html", ordery=order)

@planner_bp.route("/orders/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("planner")
def edit_transportation_order(id):
    order = TransportationOrder.query.get_or_404(id)
    form = TransportationOrderForm(obj=order)
    if form.validate_on_submit():
        try:
            order.planned_delivery_date = form.planned_delivery_date.data
            order.trailer_type = form.trailer_type.data
            order.load_weight = form.load_weight.data
            order.loading_place = form.loading_place.data
            order.deliver_place = form.delivery_place.data
            db.session.commit()
            flash("Transportation order details updated successfully.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f"Error during transportation order editing: {e}")
            flash(f"Error: {e}, try again", "danger")
        return redirect(url_for("transportation_orders"))
    return render_template("transportation_order_form.html", form=form, title="Edit Transportation Order")

@planner_bp.route("/orders/confirm-delete/<int:id>", methods=["GET"])
@login_required
@role_required("planner")
def confirm_transportation_order_delete(id):
    order = TransportationOrder.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_transportation_order_delete.html", csrf_token=csrf_token, order=order)

@planner_bp.route("/orders/delete/<int:id>", methods=["POST"])
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
    return redirect(url_for("transportation_orders"))

@planner_bp.route("/orders/archived", methods=["GET"])
@login_required
@role_required("planner")
def archived_orders_list():
    archived_orders = TransportationOrder.query.filter_by(completed=True).order_by(TransportationOrder.date).all()
    if not archived_orders:
        flash("There are any archived transportation orders", "info")
        return redirect(url_for("home"))
    return render_template("archived_transportation_orders.html", archived_orders=archived_orders)


