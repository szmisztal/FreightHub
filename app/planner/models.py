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
