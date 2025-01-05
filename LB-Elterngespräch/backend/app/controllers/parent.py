# backend/app/controllers/parent.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from model.models import Termin, db

parent_blueprint = Blueprint('parent', __name__, template_folder='templates/parent')

@parent_blueprint.route('/termine')
@login_required
def view_termine():
    termine = Termin.query.filter_by(parent_id=None).all()
    return render_template('termine.html', termine=termine)

@parent_blueprint.route('/termine/book/<int:termin_id>')
@login_required
def book_termin(termin_id):
    termin = Termin.query.get_or_404(termin_id)
    termin.parent_id = current_user.id
    db.session.commit()
    flash("Termin successfully booked!", "success")
    return redirect(url_for('parent.view_termine'))
