import enum

from sqlalchemy import Enum
from sqlalchemy.orm import relationship

from server_resources import db
from server_resources.models.user import User


class OS(enum.Enum):
    lin = 1
    win = 2
    mac = 3


class ApplicationServer(db.Model):
    __tablename__ = "application_servers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    private_address = db.Column(db.String, unique=True, nullable=False)
    os = db.Column(Enum(OS))
    ram_size = db.Column(db.Integer, nullable=False)
    cpu_cores = db.Column(db.Integer, nullable=False)
    drive_size = db.Column(db.Float, nullable=False)
    users = relationship("AppServerUser", cascade="all, delete-orphan", backref="app_servers")

    def __repr__(self):
        return '<ApplicationServer {}>'.format(self.name)


class AppServerUser(db.Model):
    __tablename__ = "app_server_users"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = relationship(User, lazy="joined")
    app_server_id = db.Column(db.Integer, db.ForeignKey("application_servers.id"), primary_key=True)
    app_server = relationship(ApplicationServer, lazy="joined")


class DatabaseServer(db.Model):
    __tablename__ = "database_servers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    private_address = db.Column(db.String(50), unique=True, nullable=False)
    db_port = db.Column(db.Integer, nullable=True)
    dbms = db.Column(db.String(10), nullable=False)
    users = relationship("DBServerUser", cascade="all, delete-orphan", backref="db_servers")

    def __repr__(self):
        return '<DatabaseServer {}>'.format(self.name)


class DBServerUser(db.Model):
    __tablename__ = "db_server_users"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = relationship(User, lazy="joined")
    db_server_id = db.Column(db.Integer, db.ForeignKey("database_servers.id"), primary_key=True)
    db_server = relationship(DatabaseServer, lazy="joined")
