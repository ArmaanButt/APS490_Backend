from app import db
from marshmallow import Schema, fields, ValidationError


class TargetModel(db.Model):
    __tablename__ = 'targets'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_working = db.Column(db.Boolean, nullable=False)
    size = db.Column(db.Float, nullable=False)
    is_enabled = db.Column(db.Boolean, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


def _not_negative(num):
    if num < 0:
        raise ValidationError('Must be greater than 0')


class TargetSchemaResource(Schema):
    id = fields.Integer(dump_only=True)
    is_working = fields.Boolean(required=True)
    size = fields.Float(validate=_not_negative, required=True)
    is_enabled = fields.Boolean(required=True)
    updated_at = fields.DateTime()


class TargetSchemaParams(Schema):
    id = fields.Integer(dump_only=True)
    is_working = fields.Boolean()
    size = fields.Float(validate=_not_negative)
    is_enabled = fields.Boolean()
    updated_at = fields.DateTime()
