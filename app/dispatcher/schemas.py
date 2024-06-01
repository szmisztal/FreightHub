from marshmallow import Schema, fields, validates, validate, ValidationError
from app.common.models import User, TransportationOrder, Trailer
from .models import TractorHead

class TractorHeadSchema(Schema):
    brand = fields.Str(required=True)
    registration_number = fields.Str(required=True, validate=validate.Length(equal=8))

class TrailerSchema(Schema):
    type = fields.Str(required=True, validate=validate.OneOf(["Curtain side",
                                                              "Refrigerated",
                                                              "Tipper",
                                                              "Low loader",
                                                              "Container",
                                                              "Self-unloading",
                                                              "Insulated"]))
    registration_number = fields.Str(required=True, validate=validate.Length(equal=7))

class DispatcherTransportationOrderSchema(Schema):
    driver = fields.Int(required=True)
    tractor_head = fields.Int(required=True)
    trailer = fields.Int(required=True)

    @validates("driver")
    def validate_driver(self, value):
        driver = User.query.filter_by(id=value, role="driver").first()
        if not driver:
            raise ValidationError("Selected driver does not exist or is not available.")
        busy_driver = TransportationOrder.query.filter_by(driver=value, completed=False).first()
        if busy_driver:
            raise ValidationError("Selected driver is currently busy.")

    @validates("tractor_head")
    def validate_tractor_head(self, value):
        tractor_head = TractorHead.query.filter_by(id=value).first()
        if not tractor_head:
            raise ValidationError("Selected tractor head does not exist or is not available.")
        busy_tractor_head = TransportationOrder.query.filter_by(tractor_head=value, completed=False).first()
        if busy_tractor_head:
            raise ValidationError("Selected tractor head is currently busy.")

    @validates("trailer")
    def validate_trailer(self, value):
        trailer = Trailer.query.filter_by(id=value).first()
        if not trailer:
            raise ValidationError("Selected trailer does not exist or is not available.")
        busy_trailer = TransportationOrder.query.filter_by(trailer=value, completed=False).first()
        if busy_trailer:
            raise ValidationError("Selected trailer is currently busy.")
