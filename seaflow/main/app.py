from flask import Flask


def register_blueprint(app):
    pass


def register_ext(app):
    from seaflow.exts import db, cors, api, mail, bcrypt
    db.init_app(app)
    cors.init_app(app)
    api.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprint(app)
    register_ext(app)
    return app
