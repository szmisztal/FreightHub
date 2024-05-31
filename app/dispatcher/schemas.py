from marshmallow import Schema, fields, validate

class TractorHeadSchema(Schema):
    brand = fields.Str(required=True)
    registration_number = fields.Str(required=True, validate=validate.Length(8))

class TrailerSchema(Schema):
    type = fields.Str(required=True, validate=validate.OneOf(["Curtain side",
                                                              "Refrigerated",
                                                              "Tipper",
                                                              "Low loader",
                                                              "Container",
                                                              "Self-unloading",
                                                              "Insulated"]))
    registration_number = fields.Str(required=True, validate=validate.Length(7))
