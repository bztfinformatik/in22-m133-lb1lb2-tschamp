import os

from flask import Flask
from model.models import db
from controllers.index import index_blueprint
from controllers.products import products_blueprint
from controllers.help import help_blueprint
from controllers.user import users_blueprint
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from model.models import User
from flask_bcrypt import Bcrypt

from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv # Umgebungsvariablen aus dem .env laden
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.secret_key = "VerySecretSecretKey"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users_blueprint.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db.init_app(app)

# hier blueprint registrieren
app.register_blueprint(index_blueprint)
app.register_blueprint(products_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(help_blueprint)

