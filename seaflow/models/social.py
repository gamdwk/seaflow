from seaflow.main.exts import db


class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    auth_id = db.Column(db.ForeignKey(''))
    reply_id = db.Column()


class Reply(db.Model):
    __tablename__ = "reply"
    id = db.Column(db.Text, nullable=False)
