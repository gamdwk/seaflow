from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful import marshal
from ..models.social import News
from ..models.auth import User
from ..main.exts import api, auth, db
from flask import g
from ..error import DbError, NotFound, NewsNotYours, ApiException
from ..fields.social import newsRes, createnewsRes, newsfield, newslikeRes
from ..fields import ResponseField
from ..helper.rediscli import news_is_like, like_news, get_like


class NewsResource(Resource):
    method_decorators = [auth.login_required()]

    def __init__(self):
        self.post_reqparse = RequestParser()
        self.post_reqparse.add_argument('content', type=str)
        self.post_reqparse.add_argument('imgs', type=list)

    def get(self, id=None, uid=None, page=1):
        me = g.user
        if id:
            t = News.query.get(id)
            uid = t.auth_id
            if t is None:
                raise NotFound
            return newsRes.marshal({
                "tid": t.id, "content": t.content, 'imgs': t.imgs,
                "uid": uid, "time": t.time
            })
        else:
            uid = uid or me['uid']
            ts = User.query.get(uid).news
            ts = ts.paginate(page=page, per_page=5)
            tss = ts.items
            x = []
            for t in tss:
                x.append(marshal({"tid": t.id, "content": t.content, 'imgs': t.imgs,
                                  "uid": uid, "time": t.time}, newsfield))
            return {"data": {'news': x, "pages": ts.pages, "current": page
                             }, 'code': 0, "message": "success"}

    def post(self):
        me = g.user
        uid = me['uid']
        try:
            news = News()
            news.auth_id = uid
            db.session.add(news)
            db.session.commit()
            tid = news.id
            args = self.post_reqparse.parse_args()
            news.init(uid, args['content'], args['imgs'])
            db.session.commit()
            return createnewsRes.marshal({'uid': uid, 'tid': tid})
        except:
            db.session.rollback()
            raise DbError

    def delete(self, id):
        me = g.user
        uid = me['uid']
        try:
            t = News.query.get(id)
            if t is None:
                raise NotFound
            if t.auth_id != uid:
                raise NewsNotYours
            db.session.delete(t)
            db.session.commit()
            return {"uid": uid, "tid": t.id}
        except ApiException as e:
            raise e
        except:
            db.session.rollback()
            raise DbError


class Like(Resource):
    method_decorators = [auth.login_required()]

    def get(self, tid):
        likes = get_like(tid)
        uid = g.user['uid']
        liked = news_is_like(uid, tid)
        return newslikeRes.marshal({
            'tid': tid,
            'uid': g.user['uid'],
            'likes': likes,
            'liked': liked
        })

    def put(self, tid):
        uid = g.user['uid']
        like_news(uid, tid)
        likes = get_like(tid)
        liked = news_is_like(uid, tid)
        return newslikeRes.marshal({
            'tid': tid,
            'uid': g.user['uid'],
            'likes': likes,
            'liked': liked
        })


class Comment(Resource):
    method_decorators = [auth.login_required()]
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass


api.add_resource(NewsResource, '/news', '/news/<int:id>',
                 '/user/<int:uid>/news/page/<int:page>')
api.add_resource(Like, '/like/news/<int:tid>')
