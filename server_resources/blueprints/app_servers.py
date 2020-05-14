from flask import Blueprint, current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from server_resources import db
from server_resources.models.server import ApplicationServer, OS
from server_resources.blueprints.auth import login_required, admin_required

blueprint = Blueprint('app_servers', __name__, url_prefix='/app_servers')


@blueprint.route('/list_app_servers')
@login_required
def list_app_servers():
    return render_template("list/app_server_list.html", servers=ApplicationServer.query.all())


@blueprint.route('/show/<name>', methods=('GET', 'POST'))
@login_required
def show(name):
    return render_template("show/app_server.html", app_server=ApplicationServer.query.filter_by(name=name).first())


@blueprint.route('/delete/<name>', methods=['POST'])
@admin_required
def delete(name):
    app_server = ApplicationServer.query.filter_by(name=name).first()
    db.session.delete(app_server)
    db.session.commit()
    return redirect(url_for('app_servers.list_app_servers'))


@blueprint.route('/update/<name>', methods=['POST'])
@admin_required
def update(name):
    app_server = ApplicationServer.query.filter_by(name=name).first()
    for key, value in request.form.items():
        if hasattr(app_server, key) and value:
            setattr(app_server, key, value) if key != 'os' else setattr(app_server, key, OS[value])
    current_app.logger.info(app_server.os)
    db.session.commit()
    return redirect(url_for('app_servers.show', name=name))


@blueprint.route("/add", methods=["POST"])
@admin_required
def add():
    param_dict = {}
    for key, value in request.form.items():
        if hasattr(ApplicationServer, key) and value:
            param_dict[key] = value if key != 'os' else OS[value]
    db.session.add(ApplicationServer(**param_dict))
    db.session.commit()
    return redirect(url_for("app_servers.list_app_servers"))

