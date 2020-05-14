from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from server_resources import db
from server_resources.models.deployment import Deployment
from server_resources.models.user import User
from server_resources.models.server import ApplicationServer, DatabaseServer
from server_resources.blueprints.auth import login_required, admin_required

blueprint = Blueprint('deployments', __name__, url_prefix='/deployments')


@blueprint.route('/list_deployments', methods=('GET', 'POST'))
@login_required
def list_deployments():
    return render_template("list/deployment_list.html",
                           deployment_list=Deployment.query.all())


@blueprint.route('/show/<name>', methods=('GET', 'POST'))
@login_required
def show(name):
    return render_template("show/deployment.html",
                           deployment=Deployment.query.filter_by(name=name).first(),
                           user_list=User.query.all(),
                           db_server_list=DatabaseServer.query.all(),
                           app_server_list=ApplicationServer.query.all())


@blueprint.route('/delete/<name>', methods=['POST'])
@admin_required
def delete(name):
    deployment = Deployment.query.filter_by(name=name).first()
    db.session.delete(deployment)
    db.session.commit()
    return redirect(url_for('deployments.list_deployments'))


@blueprint.route('/update/<name>', methods=['POST'])
@admin_required
def update(name):
    deployment = Deployment.query.filter_by(name=name).first()

    return redirect(url_for('deployments.show', name=name))


@blueprint.route("/add", methods=["POST"])
@admin_required
def add():
    name = request.form['name']
    url = request.form["url"]
    private = bool(request.form.get("private", None))
    warning = None
    if db.session.query(Deployment.query.filter_by(name=name).exists()).scalar():
        warning = f"Deployment {name} is already existing."
    elif db.session.query(Deployment.query.filter_by(url=url).exists()).scalar():
        warning = "This URL is already taken."
    if warning is None:
        db.session.add(Deployment(name=name, url=url, private=private))
        db.session.commit()
    else:
        flash(warning, 'warning')
    return redirect(url_for("deployments.list_deployments"))


@blueprint.route("/<deployment_name>/bind_user/<user_name>", methods=["POST"])
@admin_required
def bind_user(deployment_name, user_name):
    user = User.query.filter_by(name=user_name).first()
    deployment = Deployment.query.filter_by(name=deployment_name).first()
    deployment.users.append(user)
    db.session.commit()
    return redirect(url_for('deployments.show', name=deployment_name))


@blueprint.route("/<deployment_name>/unbind_user/<user_name>", methods=["POST"])
@admin_required
def unbind_user(deployment_name, user_name):
    user = User.query.filter_by(name=user_name).first()
    deployment = Deployment.query.filter_by(name=deployment_name).first()
    deployment.users.remove(user)
    db.session.commit()
    return redirect(url_for('deployments.show', name=deployment_name))


@blueprint.route("/<deployment_name>/bind_app_server/<app_server_name>", methods=["POST"])
@admin_required
def bind_app_server(deployment_name, app_server_name):
    app_server = ApplicationServer.query.filter_by(name=app_server_name).first()
    deployment = Deployment.query.filter_by(name=deployment_name).first()
    deployment.app_servers.append(app_server)
    db.session.commit()
    return redirect(url_for('deployments.show', name=deployment_name))


@blueprint.route("/<deployment_name>/unbind_app_server/<app_server_name>", methods=["POST"])
@admin_required
def unbind_app_server(deployment_name, app_server_name):
    app_server = ApplicationServer.query.filter_by(name=app_server_name).first()
    deployment = Deployment.query.filter_by(name=deployment_name).first()
    deployment.app_servers.remove(app_server)
    db.session.commit()
    return redirect(url_for('deployments.show', name=deployment_name))


@blueprint.route("/<deployment_name>/bind_db_server/<db_server_name>", methods=["POST"])
@admin_required
def bind_db_server(deployment_name, db_server_name):
    db_server = DatabaseServer.query.filter_by(name=db_server_name).first()
    deployment = Deployment.query.filter_by(name=deployment_name).first()
    deployment.db_servers.append(db_server)
    db.session.commit()
    return redirect(url_for('deployments.show', name=deployment_name))


@blueprint.route("/<deployment_name>/unbind_db_server/<db_server_name>", methods=["POST"])
@admin_required
def unbind_db_server(deployment_name, db_server_name):
    db_server = DatabaseServer.query.filter_by(name=db_server_name).first()
    deployment = Deployment.query.filter_by(name=deployment_name).first()
    deployment.db_servers.remove(db_server)
    db.session.commit()
    return redirect(url_for('deployments.show', name=deployment_name))

