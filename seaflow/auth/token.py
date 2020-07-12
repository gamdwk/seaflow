from seaflow.exts import auth
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from flask import current_app, g
from flask_restful import abort


@auth.verify_token
def verify_token(token):
    s = TimedJSONWebSignatureSerializer(
        current_app.config['secret_key']
    )
    try:
        data = s.loads(token)
    except BadSignature:
        abort(401)
    except SignatureExpired:
        abort(401)
    g.user = data['user']
    return True


def create_login_token():
    s = TimedJSONWebSignatureSerializer(
        current_app.config['secret_key']
    )