from seaflow.exts import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    _password_hash = db.Column(db.String(128))
    emil = db.Column(db.String(32), unique=True)

    @property
    def password_hash(self):
        return self._password_hash

    def hash_password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
