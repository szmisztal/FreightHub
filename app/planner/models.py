from app import db

class Company(db.Model):
    """
    Represents a company entity in the database.

    Attributes:
        id (int): The primary key of the company.
        company_name (str): The name of the company.
        country (str): The country where the company is located.
        town (str): The town where the company is located.
        postal_code (str): The postal code of the company's address.
        street (str): The street name of the company's address.
        street_number (int): The street number of the company's address.
        phone_number (str): The contact phone number of the company.
    """
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(32), nullable=False)
    town = db.Column(db.String(32), nullable=False)
    postal_code = db.Column(db.String(8), nullable=False)
    street = db.Column(db.String(32), nullable=False)
    street_number = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the company.

        Returns:
            str: A string representation of the company's details.
        """
        return f"{self.company_name} - {self.country}, {self.street} {self.street_number}, {self.postal_code} {self.town}, {self.phone_number}"



