from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from ..models.social import News, Comments, Replies
from ..models.auth import User
from ..main.exts import api, auth
from flask import g
from ..error import DbError


class NewsResource(Resource):
    method_decorators = [auth.login_required()]

    def __init__(self):
        self.post_reqparse = RequestParser()
        self.post_reqparse.add_argument('content', type=str)
        self.post_reqparse.add_argument('imgs', type=str, action="append")

    def get(self, id=None):
        if id:
            return

    def post(self):
        me = g.user
        uid = me['uid']
        try:
            me = User.query.get(uid)
            news = News()
            args = self.post_reqparse.parse_args()
            news.init(uid, args['content'], args['imgs'])
        except:
            raise DbError


class Comment(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass


api.add_resource(NewsResource, '/news', '/news/<int:id>')
