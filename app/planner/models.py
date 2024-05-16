import datetime
from app import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(32), nullable=False)
    town = db.Column(db.String(32), nullable=False)
    postal_code = db.Column(db.String(16), nullable=False)
    street = db.Column(db.String(32), nullable=False)
    street_number = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"Name: {self.company_name}" \
               f"\nCountry: {self.country}" \
               f"\nTown: {self.town}" \
               f"\nPostal code: {self.postal_code}" \
               f"\nStreet: {self.street} {self.street_number}" \
               f"\nPhone number: {self.phone_number}"

class TransportationOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.date.today, nullable=False)
    trailer_type = db.Column(db.String(16), nullable=False)
    load_weight = db.Column(db.Integer, nullable=False)
    loading_place = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    delivery_place = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    driver = db.Column(db.String, db.ForeignKey("user.id"), nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Date: {self.date}" \
               f"\nTrailer type: {self.trailer_type}" \
               f"\nLoad weight: {self.load_weight}" \
               f"\nLoading place: {self.loading_place}" \
               f"\nDelivery place: {self.delivery_place}" \
               f"\nCompleted: {self.completed}"
