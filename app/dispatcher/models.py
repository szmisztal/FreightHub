from app import db

class TractorHead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(16), nullable=False)
    registration_number = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return f"{self.brand.upper()} {self.registration_number.upper()}"

class Trailer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16), nullable=False)
    registration_number = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return f"{self.type.upper()} {self.registration_number.upper()}"
