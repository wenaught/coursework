from sqlalchemy.orm import relationship

from server_resources import db
from server_resources.models.user import User


class Deployment(db.Model):
    __tablename__ = "deployments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    url = db.Column(db.String(50), unique=True, nullable=False)
    private = db.Column(db.Boolean, default=True)
    users = relationship("DeploymentUser", cascade="all,delete-orphan", backref="deployments")

    def __repr__(self):
        return '<Deployment {}>'.format(self.name)


class DeploymentUser(db.Model):
    __tablename__ = "deployment_users"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user = relationship(User, lazy="joined")
    deployment_id = db.Column(db.Integer, db.ForeignKey("deployments.id"), primary_key=True)
    deployment = relationship(Deployment, lazy="joined")
