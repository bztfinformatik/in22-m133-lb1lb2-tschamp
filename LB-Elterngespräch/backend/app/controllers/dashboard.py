from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from model.models import Termin, db
from forms.ElterngespraechTerminForm import ElterngespraechTerminForm
from forms.DeleteTerminForm import DeleteTerminForm
from forms.EditUserForm import EditUserForm
from model.models import User, db


# Blueprint for admin dashboard
admin_dashboard_blueprint = Blueprint('admin_dashboard_blueprint', __name__)

@admin_dashboard_blueprint.route("/admin/dashboard", methods=["GET"])
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))
    return render_template('dashboards/admin_dashboard.html')

@admin_dashboard_blueprint.route("/admin/dashboard/termine", methods=["GET"])
@login_required
def admin_manage_termine():
    if current_user.role != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    termine = Termin.query.all()
    delete_form = DeleteTerminForm()  # Initialisiere das Formular
    return render_template('termin/admin_manage_termine.html', termine=termine, form=delete_form)



@admin_dashboard_blueprint.route("/admin/dashboard/users", methods=["GET"])
@login_required
def manage_users():
    if current_user.role != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    users = User.query.all()
    return render_template('users/manage_users.html', users=users)


@admin_dashboard_blueprint.route("/admin/dashboard/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    if current_user.role != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('admin_dashboard_blueprint.manage_users'))

    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data.strip()
        user.role = form.role.data
        db.session.commit()
        flash("User successfully updated!", "success")
        return redirect(url_for('admin_dashboard_blueprint.manage_users'))

    return render_template('users/edit_user.html', form=form, user=user)


@admin_dashboard_blueprint.route("/admin/dashboard/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if current_user.role != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('admin_dashboard_blueprint.manage_users'))

    db.session.delete(user)
    db.session.commit()
    flash("User successfully deleted!", "success")
    return redirect(url_for('admin_dashboard_blueprint.manage_users'))

@admin_dashboard_blueprint.route("/admin/dashboard/create_termin", methods=["GET", "POST"])
@login_required
def create_termin():
    if current_user.role != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    form = ElterngespraechTerminForm()  # Passe an dein bestehendes Formularmodell an
    if form.validate_on_submit():
        new_termin = Termin(
            title=form.title.data,
            teacher_id=current_user.id,  # Der aktuell eingeloggte Lehrer wird verknüpft
            date=form.date.data,
            description=form.description.data,
            time=form.time.data
        )
        db.session.add(new_termin)
        db.session.commit()
        flash("Termin successfully created!", "success")
        return redirect(url_for('admin_dashboard_blueprint.admin_manage_termine'))


    return render_template("termin/create_termin.html", form=form)


@admin_dashboard_blueprint.route("/admin/dashboard/edit_termin/<int:termin_id>", methods=["GET", "POST"])
@login_required
def edit_termin(termin_id):
    if current_user.role != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    termin = Termin.query.filter_by(id=termin_id, teacher_id=current_user.id).first()
    if not termin:
        flash("Termin not found or access denied.", "danger")
        return redirect(url_for('admin_dashboard_blueprint.admin_manage_termine'))

    form = ElterngespraechTerminForm(obj=termin)

    if form.validate_on_submit():
        termin.title = form.title.data.strip()
        termin.date = form.date.data
        termin.time = form.time.data
        termin.description = form.description.data.strip() if form.description.data else None

        db.session.commit()
        flash("Termin successfully updated!", "success")
        return redirect(url_for('admin_dashboard_blueprint.admin_manage_termine'))

    return render_template("termin/edit_termin.html", form=form, termin=termin)


@admin_dashboard_blueprint.route("/admin/dashboard/delete_termin/<int:termin_id>", methods=["POST"])
@login_required
def delete_termin(termin_id):
    if current_user.role not in ["admin", "teacher"]:
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    form = DeleteTerminForm(request.form)
    if not form.validate_on_submit():
        flash("Invalid CSRF token.", "danger")
        return redirect(url_for('admin_dashboard_blueprint.admin_manage_termine'))

    if current_user.role == "admin":
        termin = Termin.query.get(termin_id)  # Admin darf alle Termine löschen
    else:
        termin = Termin.query.filter_by(id=termin_id, teacher_id=current_user.id).first()  # Lehrer nur ihre eigenen

    if not termin:
        flash("Termin not found or access denied.", "danger")
        return redirect(url_for('admin_dashboard_blueprint.admin_manage_termine'))

    db.session.delete(termin)
    db.session.commit()
    flash("Termin successfully deleted!", "success")
    return redirect(url_for('admin_dashboard_blueprint.admin_manage_termine'))


@admin_dashboard_blueprint.route("/admin/dashboard/create_termin", methods=["GET", "POST"])
@login_required
def admin_create_termin():
    if current_user.role != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    form = ElterngespraechTerminForm()
    if form.validate_on_submit():
        new_termin = Termin(
            title=form.title.data,
            teacher_id=form.teacher_id.data,  # Admins können Lehrer zuweisen
            date=form.date.data,
            time=form.time.data,
            description=form.description.data
        )
        db.session.add(new_termin)
        db.session.commit()
        flash("Termin successfully created!", "succe    ss")
        return redirect(url_for('admin_dashboard_blueprint.admin_manage_termine'))

    return render_template("termin/create_termin.html", form=form)



# Blueprint for teacher dashboard
teacher_dashboard_blueprint = Blueprint('teacher_dashboard_blueprint', __name__)

@teacher_dashboard_blueprint.route("/teacher/dashboard", methods=["GET"])
@login_required
def teacher_dashboard():
    if current_user.role != "teacher":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    # Nur Termine des aktuellen Lehrers abrufen
    termine = Termin.query.filter_by(teacher_id=current_user.id).all()
    delete_form = DeleteTerminForm()  # Initialisiere das Formular
    return render_template('dashboards/teacher_dashboard.html', termine=termine, delete_form=delete_form)


@teacher_dashboard_blueprint.route("/teacher/dashboard/create_termin", methods=["GET", "POST"])
@login_required
def create_termin():
    if current_user.role != "teacher":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    form = ElterngespraechTerminForm()  # Passe an dein bestehendes Formularmodell an
    if form.validate_on_submit():
        new_termin = Termin(
            title=form.title.data,
            teacher_id=current_user.id,  # Der aktuell eingeloggte Lehrer wird verknüpft
            date=form.date.data,
            description=form.description.data,
            time=form.time.data
        )
        db.session.add(new_termin)
        db.session.commit()
        flash("Termin successfully created!", "success")
        return redirect(url_for('teacher_dashboard_blueprint.teacher_dashboard'))

    return render_template("termin/create_termin.html", form=form)


@teacher_dashboard_blueprint.route("/teacher/dashboard/edit_termin/<int:termin_id>", methods=["GET", "POST"])
@login_required
def edit_termin(termin_id):
    if current_user.role != "teacher":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    termin = Termin.query.filter_by(id=termin_id, teacher_id=current_user.id).first()
    if not termin:
        flash("Termin not found or access denied.", "danger")
        return redirect(url_for('teacher_dashboard_blueprint.teacher_dashboard'))

    form = ElterngespraechTerminForm(obj=termin)

    if form.validate_on_submit():
        termin.title = form.title.data.strip()
        termin.date = form.date.data
        termin.time = form.time.data
        termin.description = form.description.data.strip() if form.description.data else None

        db.session.commit()
        flash("Termin successfully updated!", "success")
        return redirect(url_for('teacher_dashboard_blueprint.teacher_dashboard'))

    return render_template("termin/edit_termin.html", form=form, termin=termin)


@teacher_dashboard_blueprint.route("/teacher/dashboard/delete_termin/<int:termin_id>", methods=["POST"])
@login_required
def delete_termin(termin_id):
    if current_user.role != "teacher":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    form = DeleteTerminForm(request.form)
    if not form.validate_on_submit():
        flash("Invalid CSRF token.", "danger")
        return redirect(url_for('teacher_dashboard_blueprint.teacher_dashboard'))

    termin = Termin.query.filter_by(id=termin_id, teacher_id=current_user.id).first()
    if not termin:
        flash("Termin not found or access denied.", "danger")
        return redirect(url_for('teacher_dashboard_blueprint.teacher_dashboard'))

    db.session.delete(termin)
    db.session.commit()
    flash("Termin successfully deleted!", "success")
    return redirect(url_for('teacher_dashboard_blueprint.teacher_dashboard'))


# Blueprint for parent dashboard
parent_dashboard_blueprint = Blueprint('parent_dashboard_blueprint', __name__)

@parent_dashboard_blueprint.route("/parent/dashboard", methods=["GET"])
@login_required
def parent_dashboard():
    if current_user.role != "parent":
        flash("Access denied!", "danger")
        return redirect(url_for('index_blueprint.index'))

    return render_template('dashboards/parent_dashboard.html')
