import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


USER = os.environ.get('MYSQL_USER', 'root')
PASSWORD = os.environ.get('MYSQL_PASSWORD', 'testpass')
HOSTNAME = os.environ.get('MYSQL_HOST', 'localhost')
DATABASE = os.environ.get('MYSQL_DATABASE', 'aps490')

MYSQL_SERVER = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4'%(
    USER,
    PASSWORD,
    HOSTNAME,
    DATABASE,
)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_SERVER
db = SQLAlchemy(app)
api = Api(app)

# Configure logging
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

from app.resources.User import UsersCollection, UsersDetail
from app.resources.Target import TargetsCollection, TargetsDetail
from app.resources.Session import SessionsCollection, SessionsDetail
from app.resources.Shot import ShotsCollection, ShotsDetail
from app.resources.Auth import AuthEndpoint


api.add_resource(UsersCollection, '/users')
api.add_resource(UsersDetail, '/users/<int:id>')

api.add_resource(TargetsCollection, '/targets')
api.add_resource(TargetsDetail, '/targets/<int:id>')

api.add_resource(SessionsCollection, '/sessions')
api.add_resource(SessionsDetail, '/sessions/<int:id>')

api.add_resource(ShotsCollection, '/shots')
api.add_resource(ShotsDetail, '/shots/<int:id>')

api.add_resource(AuthEndpoint, '/authenticate')
