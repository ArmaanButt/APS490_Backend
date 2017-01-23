from app import db
from marshmallow import Schema, fields


class ShotModel(db.Model):
    __tablename__ = 'shots'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('targets.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    coordinate_x = db.Column(db.Float, nullable=False)
    coordinate_y = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


class ShotSchemaResource(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    target_id = fields.Integer(required=True)
    session_id = fields.Integer(required=True)
    coordinate_x = fields.Float(required=True)
    coordinate_y = fields.Float(required=True)
    updated_at = fields.DateTime()


class ShotSchemaParams(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    target_id = fields.Integer()
    session_id = fields.Integer()
    coordinate_x = fields.Float()
    coordinate_y = fields.Float()
    updated_at = fields.DateTime()
