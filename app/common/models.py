import datetime as dt
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number} - {self.role}"

class TransportationOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)
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
        return f"Created by: {self.created_by}" \
               f"\nCreation date: {self.creation_date}" \
               f"\nPlanned delivery date: {self.planned_delivery_date}" \
               f"\nTrailer type: {self.trailer_type}" \
               f"\nTractor head: {self.tractor_head}" \
               f"\nTrailer: {self.trailer}" \
               f"\nLoad weight: {self.load_weight}" \
               f"\nLoading place: {self.loading_place}" \
               f"\nDelivery place: {self.delivery_place}" \
               f"\nDriver: {self.driver}" \
               f"\nCompleted: {self.completed}"
