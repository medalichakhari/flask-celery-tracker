from marshmallow import Schema, fields, validate


class TrackRequestSchema(Schema):
    url = fields.Url(required=True)
    keywords = fields.List(fields.Str(), required=True, validate=validate.Length(min=1))
