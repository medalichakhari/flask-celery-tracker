from marshmallow import Schema, ValidationError, fields, validates


class TrackRequestSchema(Schema):
    url = fields.Url(required=True)
    keywords = fields.List(fields.Str(), required=True)


class ScheduleRequestSchema(TrackRequestSchema):
    interval_minutes = fields.Int(missing=60)

    @validates("interval_minutes")
    def validate_interval(self, value):
        if value <= 0:
            raise ValidationError("interval_minutes must be greater than zero")
