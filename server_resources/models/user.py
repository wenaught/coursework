from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from server_resources import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True, nullable=False)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    _password = db.Column("password", db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        """Store the password as a hash for security."""
        self._password = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def __repr__(self):
        return '<User {}>'.format(self.name)
