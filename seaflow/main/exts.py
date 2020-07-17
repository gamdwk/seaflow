from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from .bp import api_bp

db = SQLAlchemy()
api = Api(prefix='/v1')
cors = CORS(origins='*')
auth = HTTPTokenAuth(scheme='JWT')
mail = Mail()
bcrypt = Bcrypt()
