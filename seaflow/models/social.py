from seaflow.main.exts import db
import datetime
from werkzeug.utils import cached_property
from ..fields.social import commentsField
from flask_restful import marshal
from ..helper.rediscli import news_is_like, get_like
from flask import g


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    __content = db.relationship('Contents', backref="news", uselist=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comments', backref="news")
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    groups = db.relationship("Group", backref="news", lazy="dynamic")

    def init(self, uid, content=None, imgs=None):
        # imgs：int list
        self.auth_id = uid
        c = Contents()
        c.init(content, imgs)
        c.news_id = self.id
        db.session.add(c)

    @cached_property
    def content(self):
        c = self.__content
        if c:
            return c.text
        return None

    @cached_property
    def imgs(self):
        c = self.__content
        if c:
            return c.imgs
        else:
            return None

    def make_fields(self, uid):
        if self.comments:
            comments = len(self.comments)
        else:
            comments = 0
        return {"tid": self.id, "content": self.content, 'imgs': self.imgs,
                "uid": uid, "time": self.time,
                'liked': news_is_like(uid, self.id), 'likes': get_like(self.id),
                "comments": comments,
                "avatar": self.auth.avatar, "username": self.auth.username,
                "sex": self.auth.sex
                }


class Comments(db.Model):
    # 动态：news,父亲评论：parent,祖先评论:同一个group
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    __content = db.relationship('Contents', backref="comments", uselist=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    auth_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 一对多自引用
    parent = db.relationship('Comments', backref="replies", remote_side=[id])
    reply_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))

    def init(self, uid, news_id=None, content=None, imgs=None, parent=None
             ):
        # imgs：int list
        self.auth_id = uid
        c = Contents()
        c.init(content, imgs)
        self.__content = c
        db.session.add(c)
        self.parent = Comments.query.get(parent)
        db.session.commit()
        if self.parent is None:
            g = Group()
            g.ancestor = self.id
            g.news_id = news_id
            self.news_id = news_id
            db.session.add(g)
            db.session.commit()
            self.group_id = g.id
        else:
            self.group_id = self.parent.group_id
            self.news_id = self.group.news_id

    @cached_property
    def content(self):
        c = self.__content
        if c:
            return c.text
        return None

    @cached_property
    def imgs(self):
        c = self.__content
        if c:
            return c.imgs
        else:
            return None

    @cached_property
    def is_ancestors(self):
        if self.parent:
            return False
        else:
            return True

    def make_field(self, uid=None):
        if uid is None:
            uid = g.user["uid"]
        if self.parent:
            parent = self.parent.id
            parentUID = self.parent.auth_id
        else:
            parent = self.id
            parentUID = None
        res = {
            'content': self.content,
            'imgs': self.imgs,
            'time': self.time,
            'uid': self.auth_id,
            'cid': self.id,
            'tid': self.news_id,
            'liked': news_is_like(uid, self.id, t=1),
            'likes': get_like(self.id, t=1),
            'parent': parent,
            "ancestor": self.group.ancestor,
            "group": self.group_id,
            "avatar": self.auth.avatar, "username": self.auth.username,
            "sex": self.auth.sex,
            "parentUID": parentUID
        }
        return res


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    ancestor = db.Column(db.Integer)
    members = db.relationship('Comments', backref="group", lazy="dynamic")
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    def make_fields(self, page=1, per_page=5, order_by=Comments.time,
                    need_ancestor=False):
        members = []
        ms = self.members.order_by(order_by).paginate(page, per_page)
        for m in ms.items:
            if m.id == self.ancestor:
                continue
            members.append(m.make_field())
        if need_ancestor:
            ancestor = Comments.query.get(self.ancestor)
            ancestor = ancestor.make_field()
        else:
            ancestor = self.ancestor
        return {
            "gid": self.id,
            "tid": self.news_id,
            "ancestor": ancestor,
            "members": members,
            "pages": ms.pages,
            "current": page
        }


class Files(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('contents.id'))

    def init(self, path, name, type):
        self.path = path
        self.name = name
        self.type = type


class Contents(db.Model):
    __tablename__ = "contents"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    __imgs = db.relationship('Files', backref="parents", lazy="dynamic")
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    comments_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    def init(self, text=None, imgs=None):
        self.text = text
        if isinstance(imgs, int):
            Files.query.get(imgs).parents = self
        elif isinstance(imgs, list):
            for img in imgs:
                Files.query.get(img).parents = self

    @cached_property
    def imgs(self):
        imgs = []
        for img in self.__imgs:
            imgs.append(img.path)
        return imgs


class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    is_url = db.Column(db.Boolean, default=False)
    from_user = db.Column(db.Integer)
    to_user = db.Column(db.Integer)
    type = db.Column(db.String(64), default="message")
    # type分为message, apply(好友申请）,notice(系统通知）
    is_send = db.Column(db.Boolean, default=False)
    agree = db.Column(db.Boolean)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def init(self, from_user, to_user, content=None, is_url=False, type="message"):
        self.from_user = from_user
        self.to_user = to_user
        self.content = content
        self.is_url = is_url
        self.type = type

    def make_fields(self):
        return {
            "mid": self.id,
            "from": self.from_user,
            "to": self.to_user,
            "content": self.content,
            "type": self.type,
            "is_url": self.is_url,
            "time": self.time,
            "agree": self.agree
        }
