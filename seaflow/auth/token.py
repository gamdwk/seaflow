from seaflow.main.exts import auth
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from flask import current_app, g, request
from datetime import timedelta
from ..helper.rediscli import get_salt
from werkzeug.exceptions import Unauthorized
from ..models.auth import User


@auth.verify_token
def verify_token(token):
    s = TimedJSONWebSignatureSerializer(
        current_app.config['SECRET_KEY']
    )
    try:
        data = s.loads(token)
        uid = data["user"]["uid"]
    except SignatureExpired:
        raise Unauthorized
    except BadSignature:
        raise Unauthorized
    salt = data["salt"]
    if salt != get_salt(uid):
        raise Unauthorized
    g.user = data['user']
    if data['type'] is 'refresh':
        if request.endpoint != "auth" or request.method != 'put':
            raise Unauthorized("token类型错误")
    g.token_type = data['type']
    return True


def create_login_token(refresh=True):
    access_serializer = TimedJSONWebSignatureSerializer(
        current_app.config['SECRET_KEY'], expires_in=timedelta(hours=1).total_seconds()
    )
    uid = g.user["uid"]
    salt = get_salt(uid)
    access_data = {
        "user": g.user,
        "type": "access",
        "salt": salt
    }
    access_token = access_serializer.dumps(access_data)
    if refresh:
        refresh_token = create_refresh_token(salt)
        return access_token.decode('ascii'), refresh_token.decode('ascii')
    else:
        return access_token.decode('ascii'), None


def create_refresh_token(salt):
    refresh_serializer = TimedJSONWebSignatureSerializer(
        current_app.config['SECRET_KEY'], expires_in=timedelta(days=10).total_seconds()
    )

    refresh_data = {
        "user": g.user,
        "type": "refresh",
        "salt": salt
    }
    refresh_token = refresh_serializer.dumps(refresh_data)
    return refresh_token


@auth.get_user_roles
def get_role(user):
    uid = g.user['uid']
    u = User.query.get(uid)
    return u.get_role()
