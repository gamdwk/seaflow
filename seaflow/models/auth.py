from seaflow.main.exts import db, bcrypt
from ..helper.rediscli import save_salt


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    _password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32), unique=True)
    sex = db.Column(db.Integer, default=2)
    introduction = db.Column(db.String(128))
    lock = db.Column(db.Boolean, default=False)
    pageBgc = db.Column(db.String(128))
    avatar = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=3)
    comments = db.relationship("Comments", backref="auth", lazy="dynamic")
    news = db.relationship("News", backref="auth", lazy="dynamic")

    @property
    def password_hash(self):
        return self._password_hash

    def hash_password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password)
        save_salt(self.id)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def init_user(self, email, password):
        self.email = email
        self.hash_password(password)
        self.username = email

    def update(self, data):
        for key, value in data.items():
            if value is None:
                continue
            else:
                self.__setattr__(key, value)

    def get_role(self):
        return self.role.name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(32), unique=True)
    users = db.relationship('User', backref="role", lazy="dynamic")

    @property
    def name(self):
        return self._name

    def ad(self, name):
        self._name = name


def create_role():
    roles = ["administrator", "auditor", "member"]
    x = 1
    for role in roles:
        try:
            r = Role()
            r.id = x
            x = x + 1
            r.ad(role)
            db.session.add(r)
            db.session.commit()
        except:
            db.session.rollback()
    try:
        u = User.query.get(0)
        if u is None:
            u = User()
            u.id = 0
        u.init_user('admin', 'admin')
        u.role_id = 1
        db.session.add(u)
        db.session.commit()
    except:
        db.session.rollback()
