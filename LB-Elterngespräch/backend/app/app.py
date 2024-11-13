import os

from flask import Flask
from model.models import db
from controllers.index import index_blueprint
from controllers.products import products_blueprint

from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv # Umgebungsvariablen aus dem .env laden
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.secret_key = "VerySecretSecretKey"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

csrf = CSRFProtect(app)

db.init_app(app)

# hier blueprint registrieren
app.register_blueprint(index_blueprint)
app.register_blueprint(products_blueprint)


