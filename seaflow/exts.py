from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from celery import Celery

db = SQLAlchemy()
api = Api()
cors = CORS()
auth = HTTPTokenAuth(scheme='JWT')
mail = Mail()
bcrypt = Bcrypt()