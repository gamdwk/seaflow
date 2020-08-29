from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful import marshal
from ..models.social import News, Comments, Group
from ..models.auth import User
from ..main.exts import api, auth, db
from flask import g
from ..error import DbError, NotFound, NewsNotYours, ApiException
from ..fields.social import newsRes, createnewsRes, newsfield, \
    newslikeRes, commentRes, GroupRes, RepliesRes
from ..fields.auth import friendsRes
from ..fields import ResponseField
from ..helper.rediscli import news_is_like, like_news, get_like
from werkzeug.exceptions import HTTPException


class NewsResource(Resource):
    method_decorators = [auth.login_required()]

    def __init__(self):
        self.post_reqparse = RequestParser()
        self.post_reqparse.add_argument('content', type=str)
        self.post_reqparse.add_argument('imgs', type=str, action="append")

    def get(self, id=None, uid=None, page=1):
        me = g.user
        if id is not None:
            t = News.query.get_or_404(id)
            uid = t.auth_id
            if t is None:
                raise NotFound
            return newsRes.marshal(
                t.make_fields(uid))
        else:
            uid = uid or me['uid']
            ts = User.query.get_or_404(uid).news
            ts = ts.order_by(-News.time)
            ts = ts.paginate(page=page, per_page=5)
            tss = ts.items
            x = []
            for t in tss:
                x.append(marshal(t.make_fields(uid), newsfield))
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
            t = News.query.get_or_404(id)
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

    def get(self, tid=None, cid=None):
        if tid is not None:
            t = 0
        elif cid is not None:
            t = 1
        tid = tid or cid
        likes = get_like(tid)
        uid = g.user['uid']
        liked = news_is_like(uid, tid, t=t)
        return newslikeRes.marshal(like_re(t, tid, likes, liked))

    def put(self, tid=None, cid=None):
        if tid is not None:
            t = 0
        elif cid is not None:
            t = 1
        tid = tid or cid
        uid = g.user['uid']
        like_news(uid, tid, t)
        likes = get_like(tid, t)
        liked = news_is_like(uid, tid, t)
        return newslikeRes.marshal(like_re(t, tid, likes, liked))


def like_re(t, id, likes, liked):
    res = {
        'uid': g.user['uid'],
        'likes': likes,
        'liked': liked
    }
    if t == 1:
        res['cid'] = id
    else:
        res['tid'] = id
    return res


class Comment(Resource):
    method_decorators = [auth.login_required()]

    def __init__(self):
        self.po_reqparse = RequestParser()
        self.po_reqparse.add_argument('tid', type=int, location=['json', 'args'])
        self.po_reqparse.add_argument('cid', type=int)
        self.po_reqparse.add_argument('content', type=str)
        self.po_reqparse.add_argument('imgs', type=int, action="append")

    def get(self, cid=None, tid=None, page=1):
        uid = g.user["uid"]
        c = Comments.query.get(cid)
        if c:
            return commentRes.marshal(c.make_field(uid))
        else:
            t = News.query.get_or_404(tid)
            cs = t.groups.paginate(page=page, per_page=5)
            replies = [c.make_fields(need_ancestor=True) for c in cs.items]
            return RepliesRes.marshal({"replies": replies, "current": page,
                                       "pages": cs.pages})

    def post(self, tid=None):
        uid = g.user["uid"]
        args = self.po_reqparse.parse_args()
        c = Comments()
        try:
            db.session.add(c)
            db.session.commit()
        except:
            db.session.rollback()
            raise DbError
        c.init(uid, news_id=args['tid'] or tid, content=args['content'],
               imgs=args['imgs'], parent=args["cid"])
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise DbError
        return commentRes.marshal(c.make_field(uid))

    def delete(self, cid):
        try:
            c = Comments.query.get_or_404(cid)
            if c is None:
                raise NotFound
            db.session.delete(c)
            db.session.commit()
        except ApiException as e:
            raise e
        except HTTPException as e:
            raise e
        except:
            db.session.rollback()
            raise DbError
        return ResponseField().marshal()


class Groups(Resource):
    method_decorators = [auth.login_required()]

    def get(self, gid, page=1):
        group = Group.query.get_or_404(gid)
        return GroupRes.marshal(group.make_fields(page=page, need_ancestor=True))


from ..main.exts import io
from ..helper.rediscli import make_alive, make_down, is_alive
from ..models.social import Messages
from .chat import make_message_send
from ..fields.social import friendsReply


class Friends(Resource):
    method_decorators = [auth.login_required()]

    def __init__(self):
        self.reparser = RequestParser()
        self.reparser.add_argument('message', type=str)

    def get(self, page=1):
        uid = g.user["uid"]
        me = User.query.get(uid)
        friends = me.friends
        friends = friends.paginate(page=page, per_page=5)
        res = [f.make_friends(uid) for f in friends]
        return friendsRes.marshal({
            "friends": res,
            "current": page,
            "pages": friends.pages
        })

    def post(self, uid):
        args = self.reparser.parse_args()
        content = args["message"]
        m = Messages()
        m.init(g.user["uid"], uid, content=content, type="apply")
        db.session.add(m)
        db.session.commit()
        if is_alive(uid):
            io.emit('chat', m.make_fields(), room=uid,
                    callback=make_message_send([m]))
        return ResponseField().marshal()

    def delete(self, uid):
        m = Messages()
        m.init(g.user["uid"], uid, content="您已被移除好友", type="notice")
        db.session.add(m)
        u = User.query.get_or_404(uid)
        u.break_up(g.user["uid"])
        db.session.commit()
        if is_alive(uid):
            io.emit('chat', m.make_fields(), room=uid,
                    callback=make_message_send([m]))
        return ResponseField().marshal()


class UntreatedFriendsMessage(Resource):
    method_decorators = [auth.login_required()]

    def get(self):
        ms = Messages.query.filter_by(type="apply", agree=None).all()
        res = [m.make_fields() for m in ms]
        return friendsReply.marshal({
            "reply": res
        })


class TreatedFriendsMessage(Resource):
    method_decorators = [auth.login_required()]

    def get(self):
        ms = Messages.query.filter(Messages.type == "apply").filter(
            Messages.agree is not None
        ).all()
        res = [m.make_fields() for m in ms]
        return friendsReply.marshal({
            "reply": res
        })


class AgreeFriends(Resource):
    method_decorators = [auth.login_required()]

    def __init__(self):
        self.reparser = RequestParser()
        self.reparser.add_argument('agree', type=bool, required=True)

    def post(self, mid):
        msg = Messages.query.get_or_404(mid)
        uid = msg.from_user
        u = User.query.get_or_404(uid)
        args = self.reparser.parse_args()
        if args["agree"]:
            u.make_friends(g.user["uid"])
        else:
            u.break_up(g.user["uid"])
        db.session.commit()
        return ResponseField().marshal()


api.add_resource(NewsResource, '/news', '/news/page/<int:page>', '/news/<int:id>',
                 '/user/<int:uid>/news/page/<int:page>')
api.add_resource(Like, '/like/news/<int:tid>', '/like/comments/<int:cid>')
api.add_resource(Comment, '/comment', '/comment/<int:cid>',
                 '/news/<int:tid>/comments', '/news/<int:tid>/comments/<int:page>')
api.add_resource(Groups, '/groups/<int:gid>', '/groups/<int:gid>/page/<int:page>')
api.add_resource(Friends, '/friends', '/friends/<int:uid>')
api.add_resource(AgreeFriends, '/friends/agree')
api.add_resource(UntreatedFriendsMessage, '/friends/not_handle')
api.add_resource(TreatedFriendsMessage, '/friends/handled')
