import bcrypt
from app import db
from marshmallow import Schema, fields, validate, ValidationError


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)
    role = db.Column(db.String(128), nullable=False)

    def verify_user(self, username, password):
        password = password.encode()

        if isinstance(self.password, str):
            self.password = self.password.encode()

        pwhash = bcrypt.hashpw(password, self.password)
        if self.username == username and self.password == pwhash:
            return self.id
        else:
            return None


def _validate_role(role):
    if role != 'general' and role != 'admin':
        raise ValidationError('Role must be admin or general')


# load: deserialize
# dump: serialize: python objects --> json

# Output Contract, Validating POST data
class UserSchemaResource(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    username = fields.String(validate=not_blank, required=True)
    password = fields.String(validate=not_blank, required=True, load_only=True)
    role = fields.String(validate=_validate_role, required=True)


# Validating query params, partial data for PATCH
class UserSchemaParams(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    username = fields.String(validate=not_blank)
    password = fields.String(validate=not_blank, load_only=True)
    role = fields.String(validate=_validate_role)
