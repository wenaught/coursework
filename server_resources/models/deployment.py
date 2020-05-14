from sqlalchemy.orm import relationship

from server_resources import db
from server_resources.models.server import DatabaseServer, ApplicationServer


deployment_users = db.Table('deployment_users',
                            db.Column("u_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
                            db.Column("d_id", db.Integer, db.ForeignKey("deployments.id"), primary_key=True))


class Deployment(db.Model):
    __tablename__ = "deployments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True, nullable=False)
    url = db.Column(db.String(50), unique=True, index=True, nullable=False)
    private = db.Column(db.Boolean, default=True)
    users = relationship("User", secondary=deployment_users, cascade="all", backref="deployments")
    db_servers = relationship(DatabaseServer, cascade="all, delete-orphan", backref='deployment')
    app_servers = relationship(ApplicationServer, cascade="all, delete-orphan", backref='deployment')

    def __repr__(self):
        return '<Deployment {}>'.format(self.name)
