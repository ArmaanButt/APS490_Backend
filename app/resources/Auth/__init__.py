from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import Schema, fields, validate, ValidationError


from app import db
from app.utils.utils import validate_data, update_model
from app.resources.User.models import UserModel
from app.resources.Target.models import TargetModel
from app.resources.Session.models import SessionModel


def _validate_role(role):
    if role != 'general' and role != 'admin':
        raise ValidationError('Role must be admin or general')


class AuthSchemaInput(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    username = fields.String(validate=not_blank, required=True)
    password = fields.String(validate=not_blank, required=True)


class AuthSchemaOutput(Schema):
    session_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    username = fields.String(required=True)
    role = fields.String(validate=_validate_role)


class CurrentSessionModel(db.Model):
    __tablename__ = 'current_session'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    current_session_id = db.Column(db.Integer, nullable=False)


schema_input = AuthSchemaInput()
schema_output = AuthSchemaOutput()


class AuthEndpoint(Resource):
    def post(self):
        params = request.get_json()
        try:
            validate_data(schema=schema_input, params=params)

            # gets user by username
            user_query = UserModel.query.filter_by(
                username=params.get('username'),
            ).first()
            if not user_query:
                resp = jsonify({'error': 'Not found!'})
                resp.status_code = 404
                return resp

            # checks if password is correct
            if params.get('password') != user_query.password:
                resp = jsonify({'error': 'Incorrect password!'})
                resp.status_code = 403
                return resp

            # there must be at least 1 target in db
            target_id = TargetModel.query.first().id
            user_id = user_query.id
            updated_at = datetime.utcnow()

            # creates a new session
            new_session = SessionModel(
                user_id=user_id,
                target_id=target_id,
                updated_at=updated_at,
            )
            db.session.add(new_session)
            db.session.commit()
            session_query = SessionModel.query.get(new_session.id)
            current_session_id = session_query.id

            # creates or updates the current session id
            current_session_query = CurrentSessionModel.query.first()
            if not current_session_query:
                new_entry = CurrentSessionModel(
                    current_session_id=current_session_id,
                )
                db.session.add(new_entry)
            else:
                new_data = {'current_session_id': current_session_id}
                update_model(resource=new_data, model=current_session_query)
            db.session.commit()

            results = schema_output.dump({
                'session_id': current_session_id,
                'user_id': user_id,
                'username': user_query.username,
                'role': user_query.role,
            }).data
            return results, 201
        except ValidationError as err:
            resp = jsonify({'error': err.messages})
            resp.status_code = 400
            return resp
