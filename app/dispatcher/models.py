from app import db

class TractorHead(db.Model):
    """
    Represents a tractor head in the system.

    Attributes:
        id (int): The primary key of the tractor head.
        brand (str): The brand of the tractor head.
        registration_number (str): The unique registration number of the tractor head.
    """
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(16), nullable=False)
    registration_number = db.Column(db.String(8), unique=True, nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the tractor head.

        Returns:
            str: A string representation of the tractor head's details.
        """
        return f"{self.brand} {self.registration_number}"
