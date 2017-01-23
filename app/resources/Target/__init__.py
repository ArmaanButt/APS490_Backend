import datetime
from flask import request, jsonify
from flask_restful import Resource

from sqlalchemy.exc import SQLAlchemyError

from app import db
from .models import TargetModel, TargetSchemaResource, TargetSchemaParams
from marshmallow import ValidationError
from app.utils.utils import update_model, validate_data, convert_to_boolean


schema_resource = TargetSchemaResource()
schema_params = TargetSchemaParams()


class TargetsCollection(Resource):
    def get(self):
        params = request.args
        try:
            validate_data(schema=schema_params, params=params)
            target_query = _build_query(params=params)
            result = schema_resource.dump(target_query, many=True).data
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
            new_target = TargetModel(
                is_working=convert_to_boolean(data.get('is_working')),
                size=data.get('size'),
                is_enabled=convert_to_boolean(data.get('is_enabled')),
                updated_at=updated_at,
            )
            db.session.add(new_target)
            db.session.commit()
            target_query = TargetModel.query.get(new_target.id)
            results = schema_resource.dump(target_query).data
            return results, 201
        except ValidationError as err:
            resp = jsonify({'error': err.messages})
            resp.status_code = 400
            return resp
        except SQLAlchemyError:
            resp = jsonify({'error': 'Something went wrong'})
            resp.status_code = 400
            return resp


class TargetsDetail(Resource):
    def get(self, id):
        target_query = TargetModel.query.filter_by(id=id).first()
        if not target_query:
            resp = jsonify({'error': 'Not found!'})
            resp.status_code = 404
            return resp
        else:
            results = schema_resource.dump(target_query).data
            return results, 200

    def patch(self, id):
        target_query = TargetModel.query.filter_by(id=id).first()
        if not target_query:
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
                update_model(new_data, target_query)
                db.session.commit()
                results = schema_resource.dump(target_query).data
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
        target_query = TargetModel.query.filter_by(id=id).first()
        if not target_query:
            resp = jsonify({'error': 'Not found!'})
            resp.status_code = 404
            return resp
        else:
            db.session.delete(target_query)
            db.session.commit()
            return '', 204


def _build_query(params):
    q = TargetModel.query
    if params.get('id'):
        q = q.filter_by(id=params.get('id'))
    if params.get('is_working'):
        q = q.filter_by(
            is_working=convert_to_boolean(params.get('is_working')),
        )
    if params.get('is_enabled'):
        q = q.filter_by(
            is_enabled=convert_to_boolean(params.get('is_enabled')),
        )
    return q
