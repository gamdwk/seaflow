from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

db = SQLAlchemy()
api = Api(catch_all_404s=True)
cors = CORS(origins='*', supports_credentials=True)
auth = HTTPTokenAuth(scheme='JWT')
mail = Mail()
bcrypt = Bcrypt()
io = SocketIO(cors_allowed_origins='*', engineio_logger=True, logger=True)