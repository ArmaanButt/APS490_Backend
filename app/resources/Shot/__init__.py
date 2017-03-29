import datetime
from flask import request, jsonify
from flask_restful import Resource

from sqlalchemy.exc import SQLAlchemyError

from app import db
from .models import ShotModel, ShotSchemaResource, ShotSchemaParams
from marshmallow import ValidationError
from app.utils.utils import validate_data, update_model
from app.resources.Auth import CurrentSessionModel


schema_resource = ShotSchemaResource()
schema_params = ShotSchemaParams()


class ShotsCollection(Resource):
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

        # need to have a current session
        current_session_query = CurrentSessionModel.query.first()
        if not current_session_query:
            resp = jsonify({'error': 'No current session'})
            resp.status_code = 400
            return resp

        try:
            updated_at = datetime.datetime.utcnow()
            new_shot = ShotModel(
                user_id=current_session_query.user_id,
                target_id=current_session_query.target_id,
                session_id=current_session_query.session_id,
                coordinate_x=data.get('coordinate_x'),
                coordinate_y=data.get('coordinate_y'),
                updated_at=updated_at,
            )
            db.session.add(new_shot)
            db.session.commit()
            shot_query = ShotModel.query.get(new_shot.id)
            results = schema_resource.dump(shot_query).data
            return results, 201
        except ValidationError as err:
            resp = jsonify({'error': err.messages})
            resp.status_code = 400
            return resp
        except SQLAlchemyError:
            resp = jsonify({'error': 'Something went wrong'})
            resp.status_code = 400
            return resp


class ShotsDetail(Resource):
    def get(self, id):
        shot_query = ShotModel.query.filter_by(id=id).first()
        if not shot_query:
            resp = jsonify({'error': 'Not found!'})
            resp.status_code = 404
            return resp
        else:
            results = schema_resource.dump(shot_query).data
            return results, 200

    def patch(self, id):
        shot_query = ShotModel.query.filter_by(id=id).first()
        if not shot_query:
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
                update_model(new_data, shot_query)
                db.session.commit()
                results = schema_resource.dump(shot_query).data
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
        shot_query = ShotModel.query.filter_by(id=id).first()
        if not shot_query:
            resp = jsonify({'error': 'Not found!'})
            resp.status_code = 404
            return resp
        else:
            db.session.delete(shot_query)
            db.session.commit()
            return '', 204


def _build_query(params):
    q = ShotModel.query
    if params.get('id'):
        q = q.filter_by(id=params.get('id'))
    if params.get('user_id'):
        q = q.filter_by(user_id=params.get('user_id'))
    if params.get('target_id'):
        q = q.filter_by(target_id=params.get('target_id'))
    if params.get('session_id'):
        q = q.filter_by(session_id=params.get('session_id'))
    return q
