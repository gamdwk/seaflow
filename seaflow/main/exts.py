from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from flask_mail import Mail
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
api = Api(catch_all_404s=True)
cors = CORS(origins='*')
auth = HTTPTokenAuth(scheme='JWT')
mail = Mail()
bcrypt = Bcrypt()
