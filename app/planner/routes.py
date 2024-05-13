from flask import render_template, redirect, url_for, flash
from app import db
from . import planner_bp
from .models import Company
from .forms import CompanyForm

@planner_bp.route("/companies/new", methods=["GET", "POST"])
def new_company():
    form = CompanyForm()
    if form.validate_on_submit():
        company = create_company(form)
        db.session.add(company)
        db.session.commit()
        flash("New company has been added.", "success")
        return redirect(url_for("home"))
    return render_template("create_company.html", form=form)

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
        flash("Companies list empty", "message")
        return redirect(url_for("home"))
    return render_template("companies_list.html", companies=all_companies)


@planner_bp.route("/companies/<int:company_id>")
def company_details(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template("company_details.html", company=company)
