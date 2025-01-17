import sqlalchemy
import sqlalchemy.orm

from flask import redirect, request, flash, url_for
from flask.templating import render_template
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask import Blueprint
from forms.UserForm import RegisterForm
from forms.UserForm import LoginForm
from model.models import User, db
from flask_bcrypt import Bcrypt
from controllers.decorater import requires_access_level
from model.ACCESS import ACCESS

bcrypt = Bcrypt()

users_blueprint = Blueprint('users_blueprint', __name__)

@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Successfully logged in!", "success")
                return redirect(url_for('users_blueprint.dashboard'))
            else:
                flash("Invalid username or password", "danger")
        else:
            flash("User not found", "warning")
    return render_template('login.html', form=form)


@users_blueprint.route("/dashboard", methods=["GET"])
@requires_access_level(ACCESS['guest'])
def dashboard():
    return render_template('dashboard.html')


@users_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('users_blueprint.login'))


@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("Username already exists", "danger")
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('users_blueprint.login'))

    return render_template('register.html', form=form)
