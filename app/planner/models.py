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
        return f"{self.company_name} - {self.country}, {self.street} {self.street_number}, {self.postal_code} {self.town}, {self.phone_number}"


