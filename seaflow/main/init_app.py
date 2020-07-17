from flask import Flask
from seaflow import register_celery


def register_blueprint(app):
    from .bp import api_bp
    from .exts import api
    app.register_blueprint(api_bp)
    api.init_app(api_bp)


def register_ext(app):
    from seaflow.main.exts import db, cors, mail, bcrypt
    db.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_celery(app)
    register_blueprint(app)
    register_ext(app)
    return app
