from flask import Flask


def register_blueprint(app):
    from .bp import api_bp
    from .exts import api
    app.register_blueprint(api_bp)
    api.init_app(api_bp)


def register_ext(app):
    from seaflow.main.exts import db, cors, mail, bcrypt, io
    db.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    io.init_app(app)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprint(app)
    register_ext(app)

    @app.before_first_request
    def first_request():
        from ..models.auth import create_role
        create_role()
    return app
