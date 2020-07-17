from seaflow.main.exts import auth
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from flask import current_app, g
from flask_restful import abort
from datetime import timedelta


@auth.verify_token
def verify_token(token):
    s = TimedJSONWebSignatureSerializer(
        current_app.config['secret_key']
    )
    data = s.loads(token)
    return data


def create_login_token(refresh=True):
    access_serializer = TimedJSONWebSignatureSerializer(
        current_app.config['secret_key'], expires_in=timedelta(hours=1).total_seconds()
    )
    access_data = {
        "user": g.user,
        "type": "access"
    }

    refresh_serializer = TimedJSONWebSignatureSerializer(
        current_app.config['secret_key'], expires_in=timedelta(days=10).total_seconds()
    )

    refresh_data = {
        "user": g.user,
        "type": "refresh"
    }
    access_token = access_serializer.dumps(g.user)
    refresh_token = refresh_serializer.dumps(g.user)
    return access_token, refresh_token
