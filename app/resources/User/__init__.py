import bcrypt
from flask import request, jsonify
from flask_restful import Resource

from sqlalchemy.exc import SQLAlchemyError

from app import db
from .models import UserModel, UserSchemaResource, UserSchemaParams
from marshmallow import ValidationError
from app.utils.utils import update_model, validate_data


schema_resource = UserSchemaResource()
schema_params = UserSchemaParams()


class UsersCollection(Resource):
    def get(self):
        params = request.args
        try:
            validate_data(schema=schema_params, params=params)
            user_query = _build_query(params=params)
            result = schema_resource.dump(user_query, many=True).data
            return result
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 400
            return resp

    def post(self):
        params = request.get_json()
        try:
            validate_data(schema=schema_resource, params=params)
            password = params.get('password').encode('utf-8')
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            new_user = UserModel(
                username=params.get('username'),
                password=hashed,
                role=params.get('role'),
            )
            db.session.add(new_user)
            db.session.commit()
            user_query = UserModel.query.get(new_user.id)
            results = schema_resource.dump(user_query).data
            return results, 201
        except ValidationError as err:
            resp = jsonify({'error': err.messages})
            resp.status_code = 400
            return resp
        except SQLAlchemyError:
            resp = jsonify({'error': 'Username already exists!'})
            resp.status_code = 409
            return resp


class UsersDetail(Resource):
    def get(self, id):
        user_query = UserModel.query.filter_by(id=id).first()
        if not user_query:
            resp = jsonify({'error': 'Not found!'})
            resp.status_code = 404
            return resp
        else:
            results = schema_resource.dump(user_query).data
            return results, 200

    def patch(self, id):
        user_query = UserModel.query.filter_by(id=id).first()
        if not user_query:
            resp = jsonify({'error': 'Not found!'})
            resp.status_code = 404
            return resp
        else:
            # validate data
            new_data = request.get_json()
            new_data['id'] = id
            try:
                validate_data(schema_params, new_data)
                update_model(new_data, user_query)
                db.session.commit()
                results = schema_resource.dump(user_query).data
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
        user_query = UserModel.query.filter_by(id=id).first()
        if not user_query:
            resp = jsonify({'error': 'Not found!'})
            resp.status_code = 404
            return resp
        else:
            db.session.delete(user_query)
            db.session.commit()
            return '', 204


def _build_query(params):
    q = UserModel.query
    if params.get('id'):
        q = q.filter_by(id=params.get('id'))
    if params.get('username'):
        q = q.filter_by(username=params.get('username'))
    if params.get('role'):
        q = q.filter_by(role=params.get('role'))
    return q
