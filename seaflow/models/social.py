from seaflow.main.exts import db
import datetime
from werkzeug.utils import cached_property


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    __content = db.relationship('Contents', backref="news", uselist=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # comments = db.relationship('Comments', backref="news", lazy="dynamic")
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

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


"""class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    __content = db.Column(db.Text, nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    replies = db.relationship('Comments', backref="parent", lazy="dynamic")
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    time = db.Column(db.DateTime, default=datetime.datetime.now())

    def init(self, content, uid, news_id, parent_id=None):
        self.auth_id = uid
        self.__content = content
        self.news_id = news_id
        if parent_id:
            self.parent_id = parent_id"""

"""class Replies(db.Model):
    __tablename__ = "replies"
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    replies = db.relationship('Comments', backref="replies", lazy="dynamic")
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    content = db.Column(db.Text, nullable=False)
"""


class Files(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(64))
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

    def init(self, text=None, imgs=None):
        self.text = text
        if isinstance(imgs, int):
            Files.query.get(imgs).parent_id = self.id
        elif isinstance(imgs, list):
            for img in imgs:
                Files.query.get(img).parent_id = self.id

    @cached_property
    def imgs(self):
        imgs = []
        for img in self.__imgs:
            imgs.append(img.path)
        return imgs
