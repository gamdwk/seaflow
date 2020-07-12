from seaflow.exts import api
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from .models import User as UserModel
from flask import g
from .token import create_login_token


class Auth(Resource):
    """用户的注册登录修改信息部分"""

    def __init__(self):
        self.reqparse = RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='username is required!')
        self.reqparse.add_argument('password', type=str, required=True,
                                   help='password is required!')
        self.reqparse.add_argument('email', type=str)

    def get(self):
        args = self.reqparse.parse_args()
        me = UserModel.query.filter_by(username=args['username']).first()
        if me is None:
            return {
                ''
            }
        if me.verify_password(args['password']):
            g.user = me
            token = create_login_token()
        else:
            return
        return token

    def post(self):
        args = self.reqparse.parse_args()
        auth = args['username']

    def put(self):
        pass

    def delete(self):
        pass


class User(Resource):
    def get(self, uid):
        UserModel.query.filter_by(id=uid)


class Email(Resource):
    def get(self):
        pass


api.add_resource(Auth, '/auth')
api.add_resource()
