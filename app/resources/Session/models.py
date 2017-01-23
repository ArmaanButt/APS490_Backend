from app import db
from marshmallow import Schema, fields


class SessionModel(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('targets.id'), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


class SessionSchemaResource(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    target_id = fields.Integer(required=True)
    updated_at = fields.DateTime()


class SessionSchemaParams(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    target_id = fields.Integer()
    updated_at = fields.DateTime()
