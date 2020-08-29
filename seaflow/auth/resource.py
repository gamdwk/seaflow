from seaflow.main.exts import api, db, auth
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from itsdangerous import BadSignature
from seaflow.models.auth import User as UserModel
from flask import g
from .token import create_login_token
from ..helper import verify_code, create_check_code, save_check_code
from ..error.auth import UserNotExist, PasswordError, UserAlreadyExist
from ..error import CodeError, ApiException, DbError
from seaflow.fields.auth import auth_response, user_response, email_response, \
    user_register_response
from seaflow.fields import common_response
from seaflow import send_async_mail

reqparse = RequestParser()
reqparse.add_argument('email', type=str, nullable=False,
                      help='email is required!')
reqparse.add_argument('password', type=str, nullable=False,
                      help='password is required!')
reqparse.add_argument('captcha', type=str, nullable=False,
                      help='captcha is required!')


class Auth(Resource):
    """用户的注册登录修改信息部分"""
    method_decorators = {'put': [auth.login_required()]}

    def __init__(self):
        self.post_reqparse = RequestParser()
        self.post_reqparse.add_argument('email', type=str, nullable=False,
                                        help='email is required!')
        self.post_reqparse.add_argument('password', type=str, nullable=False,
                                        help='password is required!')

    def post(self):
        args = self.post_reqparse.parse_args()
        try:
            me = UserModel.query.filter_by(email=args['email']).first()
        except:
            db.session.rollback()
            raise DbError
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
        if g.token_type != "refresh":
            raise ApiException(description="token类型错误")
        access_token, refresh_token = create_login_token()
        return auth_response.marshal({"access_token": access_token,
                                      "refresh_token": refresh_token})

    def delete(self):
        return


class User(Resource):
    method_decorators = {'get': [auth.login_required()],
                         'put': [auth.login_required()],
                         "delete": [auth.login_required(role="administrator")]}

    def __init__(self):
        self.reqparse = reqparse.copy()
        self.del_parse = RequestParser()
        self.del_parse.add_argument("email", type=str)
        self.del_parse.add_argument("uid", type=int)
        self.put_parse = RequestParser()
        self.put_parse.add_argument("sex", type=int, choices=[0, 1, 2])
        self.put_parse.add_argument("pageBgc", type=str)
        self.put_parse.add_argument("introduction", type=str)
        self.put_parse.add_argument("avatar", type=str)
        self.put_parse.add_argument("username", type=str)

    def get(self, uid=None):
        if uid is None:
            u = g.user
            uid = u['uid']
        try:
            u = UserModel.query.get(uid)
        except:
            raise DbError
        if u is None:
            raise UserNotExist
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
        db.session.add(u)
        try:
            db.session.commit()
            u.init_user(email, password)
            db.session.commit()
        except:
            db.session.rollback()
            raise ApiException(description="注册失败", code=404)
        return user_register_response.marshal({'email': email, 'uid': u.id})

    def put(self):
        args = self.put_parse.parse_args(strict=True)
        try:
            uid = g.user["uid"]
            u = UserModel.query.get(uid)
            u.update(args)
            db.session.commit()
            u = UserModel.query.get(uid)
            return user_response.marshal(u.__dict__)
        except:
            db.session.rollback()
            raise DbError

    def delete(self):
        args = self.del_parse.parse_args()
        try:
            if args['uid']:
                u = UserModel.query.get(args["uid"])
            else:
                u = UserModel.query.filter_by(email=args["email"]).first()
            if u is None:
                return {"code": 404, "message": "用户不存在"}, 404
            db.session.delete(u)
            db.session.commit()
            return {"code": 0, "message": "删除成功"}
        except:
            db.session.rollback()
            raise DbError


class Email(Resource):

    def __init__(self):
        self.reqparse = RequestParser()
        self.reqparse.add_argument('email', type=str, nullable=False)
        self.reqparse.add_argument('subject', type=int, nullable=False,
                                   choices=[0, 1])

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


class Password(Resource):
    """重置密码"""

    def __init__(self):
        self.reqparse = reqparse.copy()

    def put(self):
        args = self.reqparse.parse_args()
        email = args['email']
        password = args['password']
        code = args["captcha"]
        if not verify_code(email, code):
            raise CodeError()
        try:
            me = UserModel.query.filter_by(email=args['email']).first()
        except:
            db.session.rollback()
            raise ApiException()
        if me is None:
            raise UserNotExist(code=401)
        me.hash_password(password)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise ApiException(description="注册失败", code=404)
        return common_response.marshal()


class PasswordWhenLogin(Resource):
    """修改密码"""
    method_decorators = [auth.login_required()]

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('old_password', type=str, required=True,
                                 nullable=False)
        self.parser.add_argument('new_password', type=str, required=True)

    def put(self):
        args = self.parser.parse_args()
        uid = g.user['uid']
        old_password = args["old_password"]
        new_password = args["new_password"]
        u = UserModel.query.get(uid)
        if not u.verify_password(old_password):
            raise PasswordError
        try:
            u.hash_password(new_password)
            db.session.commit()
            access_token, refresh_token = create_login_token()
            return auth_response.marshal({"access_token": access_token,
                                          "refresh_token": refresh_token})
        except:
            db.session.rollback()
            raise DbError


api.add_resource(Auth, '/auth', endpoint='auth')
api.add_resource(Email, '/email', endpoint='email')
api.add_resource(User, '/user', '/user/uid/<int:uid>', endpoint="user")
api.add_resource(Password, '/user/password', endpoint="password")
api.add_resource(PasswordWhenLogin, '/password')
