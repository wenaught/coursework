import functools
import random
import string
import smtplib
import ssl

from flask import Blueprint, current_app
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from server_resources import db
from server_resources.models.user import User

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


def admin_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user.admin:
            flash('Unauthorized access', 'warning')
            return redirect(url_for("index"))
        return view(**kwargs)
    return wrapped_view


@blueprint.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id is not None else None


@blueprint.route("/request_access", methods=["GET", "POST"])
def request_access():
    if request.method == "POST":
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
            return redirect(url_for("auth.login"))
        flash(warning, 'warning')
    return render_template("auth/request_access.html")


@blueprint.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        warning = None
        user = User.query.filter_by(email=email).first()
        if user is None:
            warning = "Incorrect username."
        elif not user.check_password(password):
            warning = "Incorrect password."
        if warning is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))
        flash(warning, 'warning')
    return render_template("auth/login.html")


@blueprint.route("/restore", methods=("GET", "POST"))
def restore():
    if request.method == "POST":
        email = request.form["email"]
        new_password = ''.join(random.sample(string.ascii_letters, 10))
        user = User.query.filter_by(email=email).first()
        user.password = new_password

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            sender_email = current_app.config['EMAIL']
            sender_password = current_app.config['EMAIL_PASSWORD']
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, new_password)
        flash("Email with new password sent", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/restore.html")


@blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
