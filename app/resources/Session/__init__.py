import datetime
from flask import request, jsonify
from flask_restful import Resource

from sqlalchemy.exc import SQLAlchemyError

from app import db
from .models import SessionModel, SessionSchemaResource, SessionSchemaParams
from marshmallow import ValidationError
from app.utils.utils import validate_data, update_model


schema_resource = SessionSchemaResource()
schema_params = SessionSchemaParams()


class SessionsCollection(Resource):
    def get(self):
        params = request.args
        try:
            validate_data(schema=schema_params, params=params)
            session_query = _build_query(params=params)
            result = schema_resource.dump(session_query, many=True).data
            return result
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 400
            return resp

    def post(self):
        data = request.get_json()
        try:
            validate_data(schema=schema_resource, params=data)
            updated_at = datetime.datetime.utcnow()
            new_session = SessionModel(
                user_id=data.get('user_id'),
                target_id=data.get('target_id'),
                updated_at=updated_at,
            )
            db.session.add(new_session)
            db.session.commit()
            session_query = SessionModel.query.get(new_session.id)
            results = schema_resource.dump(session_query).data
            return results, 201
        except ValidationError as err:
            resp = jsonify({'error': err.messages})
            resp.status_code = 400
            return resp
        except SQLAlchemyError:
            resp = jsonify({'error': 'Something went wrong'})
            resp.status_code = 400
            return resp


class SessionsDetail(Resource):
    def get(self, id):
        session_query = SessionModel.query.filter_by(id=id).first()
        if not session_query:
            resp = jsonify({'error': 'Not found!'})
            resp.status_code = 404
            return resp
        else:
            results = schema_resource.dump(session_query).data
            return results, 200

    def patch(self, id):
        session_query = SessionModel.query.filter_by(id=id).first()
        if not session_query:
            resp = jsonify({'error': 'Not found!'})
            resp.status_code = 404
            return resp
        else:
            # validate data
            new_data = request.get_json()
            new_data['id'] = id
            try:
                validate_data(schema=schema_params, params=new_data)
                updated_at = datetime.datetime.utcnow()
                new_data['updated_at'] = updated_at
                update_model(new_data, session_query)
                db.session.commit()
                results = schema_resource.dump(session_query).data
                return results, 200
            except ValidationError as err:
                resp = jsonify({'error': err.messages})
                resp.status_code = 400
                return resp
            except SQLAlchemyError:
                resp = jsonify({'error': 'Something went wrong'})
                resp.status_code = 400
                return resp

    def delete(self, id):
        session_query = SessionModel.query.filter_by(id=id).first()
        if not session_query:
            resp = jsonify({'error': 'Not found!'})
            resp.status_code = 404
            return resp
        else:
            db.session.delete(session_query)
            db.session.commit()
            return '', 204


def _build_query(params):
    q = SessionModel.query
    if params.get('id'):
        q = q.filter_by(id=params.get('id'))
    if params.get('user_id'):
        q = q.filter_by(user_id=params.get('user_id'))
    if params.get('target_id'):
        q = q.filter_by(target_id=params.get('target_id'))
    return q
