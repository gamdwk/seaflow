from seaflow.main.exts import db, bcrypt


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    _password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32), unique=True)
    sex = db.Column(db.Integer, default=2)
    introduction = db.Column(db.String(128))
    lock = db.Column(db.Boolean, default=False)
    pageBgc = db.Column(db.String(64))
    avatar = db.Column(db.String(64))

    @property
    def password_hash(self):
        return self._password_hash

    def hash_password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def init(self, email, password):
        self.email = email
        self.hash_password(password)
        self.username = email


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
