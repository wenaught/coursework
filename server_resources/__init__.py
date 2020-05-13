from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

from server_resources.models.user import User
from server_resources.models.deployment import Deployment, DeploymentUser
from server_resources.models.server import ApplicationServer, AppServerUser, DatabaseServer, DBServerUser
