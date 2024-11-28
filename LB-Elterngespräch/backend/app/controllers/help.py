from flask import Blueprint, render_template

# Blueprint für Help-Seite
help_blueprint = Blueprint('help_blueprint', __name__)

@help_blueprint.route("/help", methods=["GET"])
def help():
    """
    Zeigt eine statische Hilfeseite an.
    """
    return render_template('help.html')
