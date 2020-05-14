import enum

from sqlalchemy import Enum

from server_resources import db


class OS(enum.Enum):
    lin = 1
    win = 2
    mac = 3


class ApplicationServer(db.Model):
    __tablename__ = "application_servers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True, nullable=False)
    private_address = db.Column(db.String, unique=True, index=True, nullable=False)
    os = db.Column(Enum(OS))
    ram_size = db.Column(db.Integer, nullable=False)
    cpu_cores = db.Column(db.Integer, nullable=False)
    drive_size = db.Column(db.Float, nullable=False)
    deployment_id = db.Column(db.Integer, db.ForeignKey('deployments.id'))

    def __repr__(self):
        return '<ApplicationServer {}>'.format(self.name)


class DatabaseServer(db.Model):
    __tablename__ = "database_servers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    private_address = db.Column(db.String(50), unique=True, nullable=False)
    db_port = db.Column(db.Integer, nullable=True)
    dbms = db.Column(db.String(10), nullable=False)
    storage_size = db.Column(db.Float, nullable=False)
    deployment_id = db.Column(db.Integer, db.ForeignKey('deployments.id'))

    def __repr__(self):
        return '<DatabaseServer {}>'.format(self.name)
