# backend/app/controllers/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from model.models import User, Termin, db
from controllers.decorater import role_required

admin_blueprint = Blueprint('admin', __name__, template_folder='templates/admin')

@admin_blueprint.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    users = User.query.all()
    termine = Termin.query.all()
    return render_template('admin_dashboard.html', users=users, termine=termine)

@admin_blueprint.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.role = request.form['role']
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('edit_user.html', user=user)
