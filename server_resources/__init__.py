from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from server_resources.blueprints import auth, users, app_servers, db_servers, deployments
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(users.blueprint)
    app.register_blueprint(app_servers.blueprint)
    app.register_blueprint(db_servers.blueprint)
    app.register_blueprint(deployments.blueprint)

    app.config.from_json('config.json')

    db.init_app(app)
    from server_resources.models.user import User
    from server_resources.models.server import ApplicationServer, DatabaseServer
    from server_resources.models.deployment import Deployment
    db.create_all(app=app)

    @app.route('/')
    def index():
        return render_template("index.html")

    return app
