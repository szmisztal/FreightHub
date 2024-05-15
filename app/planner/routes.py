from flask import render_template, redirect, url_for, flash
from flask_wtf.csrf import generate_csrf
from app import db
from . import planner_bp
from .models import Company, TransportationOrder
from .forms import CompanyForm, TransportationOrderForm

@planner_bp.route("/companies/new", methods=["GET", "POST"])
def new_company():
    form = CompanyForm()
    if form.validate_on_submit():
        company = create_company(form)
        db.session.add(company)
        db.session.commit()
        flash("New company has been added.", "success")
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
def companies():
    all_companies = Company.query.all()
    if not all_companies:
        flash("Companies list is empty.", "info")
        return render_template("companies_list.html", companies=all_companies)
    return render_template("companies_list.html", companies=all_companies)


@planner_bp.route("/companies/<int:company_id>", methods=["GET"])
def company_details(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template("company_details.html", company=company)

@planner_bp.route("/companies/edit/<int:id>", methods=["GET", "POST"])
def edit_company(id):
    company = Company.query.get_or_404(id)
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        company.name = form.company_name.data
        company.country = form.country.data
        company.town = form.town.data
        company.postal_code = form.postal_code.data
        company.street = form.street.data
        company.street_number = form.street_number.data
        company.phone_number = form.phone_number.data
        db.session.commit()
        flash("Company details updated successfully.", "success")
        return redirect(url_for("companies"))
    return render_template("company_form.html", form=form, title="Edit Company")

@planner_bp.route("/companies/delete/<int:id>", methods=["POST"])
def delete_company(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    flash("Company has been deleted.", "success")
    return redirect(url_for("companies"))

@planner_bp.route("/companies/confirm-delete/<int:id>", methods=["GET"])
def confirm_company_delete(id):
    company = Company.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_company_delete.html", csrf_token = csrf_token, company=company)

@planner_bp.route("/orders/new", methods=["GET", "POST"])
def new_transportation_order():
    form = TransportationOrderForm()
    if form.validate_on_submit():
        order = create_order(form)
        db.session.add(order)
        db.session.commit()
        flash("New transportation order has been created.", "success")
        return redirect(url_for("home"))
    return render_template("transportation_order_form.html", form=form, title="New Transportation Order")

def create_order(form):
    return TransportationOrder(
        trailer_type=form.trailer_type.data,
        load_weight=form.load_weight.data,
        loading_place=form.loading_place.data,
        delivery_place=form.delivery_place.data
    )

@planner_bp.route("/orders", methods=["GET"])
def transportation_orders():
    all_orders = TransportationOrder.query.all()
    if not all_orders:
        flash("Orders list is empty.", "info")
        return render_template("transportation_orders_list.html", orders=all_orders)
    return render_template("transportation_orders_list.html", orders=all_orders)

@planner_bp.route("/orders/<int:order_id>", methods=["GET"])
def transportation_order_details(order_id):
    order = TransportationOrder.query.get_or_404(order_id)
    return render_template("transportation_order_details.html", ordery=order)

@planner_bp.route("/orders/edit/<int:id>", methods=["GET", "POST"])
def edit_transportation_order(id):
    order = TransportationOrder.query.get_or_404(id)
    form = TransportationOrderForm(obj=order)
    if form.validate_on_submit():
        order.trailer_type = form.trailer_type.data
        order.load_weight = form.load_weight.data
        order.loading_place = form.loading_place.data
        order.deliver_place = form.delivery_place.data
        db.session.commit()
        flash("Transportation order details updated successfully.", "success")
        return redirect(url_for("transportation_orders"))
    return render_template("transportation_order_form.html", form=form, title="Edit Transportation Order")

@planner_bp.route("/orders/delete/<int:id>", methods=["POST"])
def delete_transportation_order(id):
    order = TransportationOrder.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    flash("Transportation order has been deleted.", "success")
    return redirect(url_for("transportation_orders"))

@planner_bp.route("/orders/confirm-delete/<int:id>", methods=["GET"])
def confirm_transportation_order_delete(id):
    order = TransportationOrder.query.get_or_404(id)
    csrf_token = generate_csrf()
    return render_template("confirm_transportation_order_delete.html", csrf_token = csrf_token, order=order)
