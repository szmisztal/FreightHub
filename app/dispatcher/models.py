from app import db

class TractorHead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(16), nullable=False)
    registration_number = db.Column(db.String(8), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.brand} {self.registration_number}"

