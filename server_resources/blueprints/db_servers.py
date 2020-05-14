from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from server_resources import db
from server_resources.models.server import DatabaseServer
from server_resources.blueprints.auth import login_required, admin_required

blueprint = Blueprint('db_servers', __name__, url_prefix='/db_servers')


@blueprint.route('/list_db_servers', methods=('GET', 'POST'))
@login_required
def list_db_servers():
    return render_template("list/db_server_list.html", servers=DatabaseServer.query.all())


@blueprint.route('/show/<name>', methods=('GET', 'POST'))
@login_required
def show(name):
    return render_template("show/db_server.html", db_server=DatabaseServer.query.filter_by(name=name).first())


@blueprint.route('/delete/<name>', methods=['POST'])
@admin_required
def delete(name):
    db_server = DatabaseServer.query.filter_by(name=name).first()
    db.session.delete(db_server)
    db.session.commit()
    return redirect(url_for('db_servers.list_db_servers'))


@blueprint.route('/update/<name>', methods=['POST'])
@admin_required
def update(name):
    db_server = DatabaseServer.query.filter_by(name=name).first()
    for key, value in request.form.items():
        if hasattr(db_server, key) and value:
            setattr(db_server, key, value)
    db.session.commit()
    return redirect(url_for('db_servers.show', name=name))


@blueprint.route("/add", methods=["POST"])
@admin_required
def add():
    params_dict = {key: value for key, value in request.form.items() if hasattr(DatabaseServer, key)}
    db.session.add(DatabaseServer(**params_dict))
    db.session.commit()
    return redirect(url_for("db_servers.list_db_servers"))

