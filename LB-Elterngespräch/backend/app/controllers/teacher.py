# backend/app/controllers/teacher.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from model.models import Termin, db
from controllers.decorater import role_required

teacher_blueprint = Blueprint('teacher', __name__, template_folder='templates/teacher')

@teacher_blueprint.route('/teacher/termine')
@login_required
@role_required('teacher')
def teacher_termine():
    termine = Termin.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher_termine.html', termine=termine)

@teacher_blueprint.route('/teacher/termine/add', methods=['GET', 'POST'])
@login_required
@role_required('teacher')
def add_termin():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        new_termin = Termin(title=title, date=date, teacher_id=current_user.id)
        db.session.add(new_termin)
        db.session.commit()
        flash("Termin successfully added!", "success")
        return redirect(url_for('teacher.teacher_termine'))
    return render_template('add_termin.html')
