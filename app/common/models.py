from datetime import date
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    """
    Represents a user in the system.

    Attributes:
        id (int): The primary key of the user.
        username (str): The unique username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        phone_number (str): The contact phone number of the user.
        email (str): The unique email address of the user.
        password_hash (str): The hashed password of the user.
        role (str): The role of the user (e.g., planner, dispatcher, driver).
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: A string representation of the user's details.
        """
        return f"{self.first_name} {self.last_name} - {self.email}, {self.phone_number}"

class TransportationOrder(db.Model):
    """
    Represents a transportation order in the system.

    Attributes:
        id (int): The primary key of the order.
        creation_date (date): The date when the order was created.
        created_by (int): The ID of the user who created the order.
        planned_delivery_date (date): The planned delivery date for the order.
        trailer_type (str): The type of trailer required for the order.
        tractor_head (int): The ID of the assigned tractor head.
        trailer (int): The ID of the assigned trailer.
        load_weight (int): The weight of the load.
        loading_place (int): The ID of the company where the load will be loaded.
        delivery_place (int): The ID of the company where the load will be delivered.
        driver (int): The ID of the assigned driver.
        completed (bool): Whether the order has been completed.
    """
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.Date, default=date.today, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planned_delivery_date = db.Column(db.Date, nullable=False)
    trailer_type = db.Column(db.String(16), nullable=False)
    tractor_head = db.Column(db.Integer, db.ForeignKey("tractor_head.id"), nullable=True)
    trailer = db.Column(db.Integer, db.ForeignKey("trailer.id"), nullable=True)
    load_weight = db.Column(db.Integer, nullable=False)
    loading_place = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    delivery_place = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    driver = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    completed = db.Column(db.Boolean, default=False)

    creator = db.relationship("User", backref="created_orders", foreign_keys=[created_by])
    assigned_driver = db.relationship("User", backref="assigned_orders", foreign_keys=[driver])
    assigned_tractor_head = db.relationship("TractorHead", backref="assigned_orders", foreign_keys=[tractor_head])
    assigned_trailer = db.relationship("Trailer", backref="assigned_orders", foreign_keys=[trailer])
    loading_company = db.relationship("Company", backref="loading_orders", foreign_keys=[loading_place])
    delivery_company = db.relationship("Company", backref="delivery_orders", foreign_keys=[delivery_place])

    def __repr__(self):
        """
        Returns a string representation of the transportation order.

        Returns:
            str: A string representation of the order's details.
        """
        return (
            f"Created by: {self.created_by}\n"
            f"Creation date: {self.creation_date}\n"
            f"Planned delivery date: {self.planned_delivery_date}\n"
            f"Trailer type: {self.trailer_type}\n"
            f"Tractor head: {self.tractor_head}\n"
            f"Trailer: {self.trailer}\n"
            f"Load weight: {self.load_weight}\n"
            f"Loading place: {self.loading_place}\n"
            f"Delivery place: {self.delivery_place}\n"
            f"Driver: {self.driver}\n"
            f"Completed: {self.completed}"
        )

class Trailer(db.Model):
    """
    Represents a trailer in the system.

    Attributes:
        id (int): The primary key of the trailer.
        type (str): The type of the trailer.
        registration_number (str): The unique registration number of the trailer.
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16), nullable=False)
    max_load_capacity = db.Column(db.Integer, nullable=False)
    registration_number = db.Column(db.String(7), unique=True, nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the trailer.

        Returns:
            str: A string representation of the trailer's details.
        """
        return f"{self.type} {self.max_load_capacity} {self.registration_number}"
