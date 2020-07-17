from seaflow.main.exts import api, db, auth
from flask_restful import Resource, marshal
from flask_restful.reqparse import RequestParser
from .models import User as UserModel
from flask import g, render_template, current_app
from .token import create_login_token
from ..helper import verify_code, create_check_code, save_check_code, send_mail
from ..error.auth import UserNotExist, PasswordError, UserAlreadyExist
from ..error import CodeError
from .fields import auth_response, user_response, email_response
from seaflow import send_async_mail


class Auth(Resource):
    """用户的注册登录修改信息部分"""
    method_decorators = {'put': auth.login_required()}

    def __init__(self):
        self.post_reqparse = RequestParser()
        self.post_reqparse.add_argument('email', type=str, nullable=False,
                                        help='email is required!')
        self.post_reqparse.add_argument('password', type=str, nullable=False,
                                        help='password is required!')

    def post(self):
        args = self.post_reqparse.parse_args()
        me = UserModel.query.filter_by(email=args['email']).first()
        if me is None:
            raise UserNotExist
        if not me.verify_password(password=args['password']):
            raise PasswordError
        g.user = {
            "uid": me.id,
            "username": me.username
        }
        access_token, refresh_token = create_login_token()
        return auth_response.marshal({"access_token": access_token,
                                      "refresh_token": refresh_token})

    def put(self):
        g.user = auth.current_user()
        access_token, refresh_token = create_login_token()
        return auth_response.marshal({"access_token": access_token,
                                      "refresh_token": refresh_token})


class User(Resource):
    method_decorators = {'get': auth.login_required}

    def __init__(self):
        self.reqparse = RequestParser()
        self.reqparse.add_argument('email', type=str, nullable=False,
                                   help='email is required!')
        self.reqparse.add_argument('password', type=str, nullable=False,
                                   help='password is required!')
        self.reqparse.add_argument('captcha', type=str, nullable=False,
                                   help='captcha is required!')

    def get(self, uid=None):
        if uid is None:
            u = auth.current_user()
            uid = u['uid']
        else:
            u = UserModel.query.get(id=uid)
        data = u.__dict__
        data['uid'] = uid
        return user_response.marshal(data)

    def post(self):
        args = self.reqparse.parse_args()
        email = args['email']
        password = args['password']
        code = args["captcha"]
        if not verify_code(email, code):
            raise CodeError
        me = UserModel.query.filter_by(email=args['email']).first()
        if me:
            raise UserAlreadyExist
        u = UserModel()
        u.init(email, password)
        db.session.add(u)
        db.session.commit()
        return user_response.marshal({'email': email, 'uid': u.id})


class Email(Resource):
    method_decorators = [auth.login_required()]

    def __init__(self):
        self.reqparse = RequestParser()
        self.reqparse.add_argument('email', type=str, nullable=False,
                                   help='email is required!')
        self.reqparse.add_argument('subject', type=int, nullable=False,
                                   choices=[0, 1], help='subject error')

        self.subject_dict = {
            0: 'register',
            1: 'reset'
        }

    def post(self):
        args = self.reqparse.parse_args()
        email = args['email']
        subject = args['subject']
        code = create_check_code()
        save_check_code(email, code)
        send_async_mail.delay(subject=self.subject_dict[subject],
                              recipients=[email], body='验证码：' + code)
        return email_response.marshal({"email": email})


api.add_resource(Auth, '/auth', endpoint='auth')
api.add_resource(Email, '/email', endpoint='email')
api.add_resource(User, '/user', endpoint="user")
