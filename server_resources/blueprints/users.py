from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from server_resources import db
from server_resources.models.user import User
from server_resources.blueprints.auth import login_required

blueprint = Blueprint('users', __name__, url_prefix='/users')


@blueprint.route('/list_users', methods=('GET', 'POST'))
@login_required
def list_users():
    if g.user.admin:
        return render_template("list/user_list.html", user_list=User.query.all())
    else:
        flash("Unauthorized access", "warning")
        return redirect(url_for("index"))


@blueprint.route('/show/<name>', methods=('GET', 'POST'))
@login_required
def show(name):
    return render_template("show/user.html", user=User.query.filter_by(name=name).first())


@blueprint.route('/delete/<name>', methods=['POST'])
@login_required
def delete(name):
    user = User.query.filter_by(name=name).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.list_users'))


@blueprint.route('/update/<name>', methods=['POST'])
@login_required
def update(name):
    user = User.query.filter_by(name=name).first()
    email = request.form.get("email", None)
    password = request.form["password"]
    new_password = request.form.get("new_password", None)
    warning = None
    if not email and not new_password:
        warning = "Change at least one value"
    if not user.check_password(password):
        warning = "Incorrect password"
    if warning:
        flash(warning, 'warning')
        return redirect(url_for('users.show', name=name))
    if email:
        user.email = email
    if new_password:
        user.password = new_password
    db.session.commit()
    return redirect(url_for('users.show', name=name))


@blueprint.route("/add", methods=["POST"])
def add():
    email = request.form["email"]
    name = request.form['name']
    password = request.form["password"]
    warning = None
    if db.session.query(User.query.filter_by(name=name).exists()).scalar():
        warning = f"User {name} is already registered."
    elif db.session.query(User.query.filter_by(email=email).exists()).scalar():
        warning = "This email is already registered."
    if warning is None:
        db.session.add(User(name=name, email=email, password=password))
        db.session.commit()
        return redirect(url_for("users.list_users"))
    flash(warning, 'warning')
    return redirect(url_for("users.list_users"))
