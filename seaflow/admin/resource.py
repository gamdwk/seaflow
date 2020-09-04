from flask_restful import Resource
from ..main.exts import auth, db, api
from ..fields.auth import userListRes, user_response
from ..models.auth import User
from ..error import DbError
from ..error.auth import UserNotExist, UserAlreadyExist
from flask_restful.reqparse import RequestParser


class UserAdmin(Resource):
    method_decorators = [auth.login_required(role='administrator')]

    def __init__(self):
        self.del_parse = RequestParser()
        self.del_parse.add_argument("email", type=str)
        self.del_parse.add_argument("uid", type=int)
        self.post_parser = RequestParser()
        self.post_parser.add_argument("email", type=str, required=True)
        self.post_parser.add_argument("password", type=str, required=True)

    def get(self, page=1):
        us = User.query.paginate(page=page, per_page=10)
        users = [u.make_fields() for u in us.items]
        return userListRes.marshal({"users": users,
                                    "pages": us.pages,
                                    "current": us.page})

    def post(self):
        args = self.post_parser.parse_args()
        email = args["email"]
        password = args["password"]
        if User.query.filter_by(email=email).first() is not None:
            raise UserAlreadyExist
        u = User()
        db.session.add(u)
        db.session.commit()
        u.init_user(email, password)
        db.session.commit()
        return user_response.marshal(u.make_fields())

    def delete(self):
        args = self.del_parse.parse_args()
        try:
            if args['uid']:
                u = User.query.get(args["uid"])
            else:
                u = User.query.filter_by(email=args["email"]).first()
            if u is None:
                raise UserNotExist
            db.session.delete(u)
            db.session.commit()
            return {"code": 0, "message": "success"}
        except:
            db.session.rollback()
            raise DbError


class Lock(Resource):
    method_decorators = [auth.login_required(role=['administrator', 'auditor'])]


def register_admin_api():
    api.add_resource(UserAdmin, '/admin/user/pages/<int:page>',
                     '/admin/user')
