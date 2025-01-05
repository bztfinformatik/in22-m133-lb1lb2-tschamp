from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from model.models import Termin, User, db
from forms.ElterngespraechTerminForm import ElterngespraechTerminForm
from forms.DeleteTerminForm import DeleteTerminForm

termine_blueprint = Blueprint('termine_blueprint', __name__)

# Helper: Restrict access to admin users
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != "admin":
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("termine_blueprint.termine"))
        return f(*args, **kwargs)
    return decorated_function

# Route: List all Termine
@termine_blueprint.route("/termine", methods=["GET"])
@login_required
def termine():
    termine = db.session.query(Termin).order_by(Termin.date, Termin.teacher_id).all()
    return render_template("termin/termine.html", termine=termine)

# Route: Add a new Termin
@termine_blueprint.route("/termine/add", methods=["GET", "POST"])
@login_required
@admin_required
def termine_add():
    form = ElterngespraechTerminForm()
    teachers = db.session.query(User).filter_by(role="teacher").order_by(User.username).all()
    form.lehrer_id.choices = [(teacher.id, teacher.username) for teacher in teachers]

    if form.validate_on_submit():
        new_termin = Termin(
            title=form.title.data,
            teacher_id=form.lehrer_id.data,
            date=form.date.data,
            time=form.time.data,
            description=form.description.data,
        )
        db.session.add(new_termin)
        db.session.commit()
        flash("Termin successfully added!", "success")
        return redirect(url_for("termine_blueprint.termine"))

    return render_template("termin/termin_add.html", form=form)

# Route: Edit an existing Termin
@termine_blueprint.route("/termine/edit/<int:termin_id>", methods=["GET", "POST"])
@login_required
@admin_required
def termine_edit(termin_id):
    termin = db.session.query(Termin).filter_by(id=termin_id).first()
    if not termin:
        flash("Termin not found.", "danger")
        return redirect(url_for("termine_blueprint.termine"))

    form = ElterngespraechTerminForm(obj=termin)
    teachers = db.session.query(User).filter_by(role="teacher").order_by(User.username).all()
    form.lehrer_id.choices = [(teacher.id, teacher.username) for teacher in teachers]

    if form.validate_on_submit():
        termin.title = form.title.data
        termin.teacher_id = form.lehrer_id.data
        termin.date = form.date.data
        termin.time = form.time.data
        termin.description = form.description.data

        db.session.commit()
        flash("Termin successfully updated!", "success")
        return redirect(url_for("termine_blueprint.termine"))

    return render_template("termin/termin_edit.html", form=form, termin=termin)

# Route: Delete a Termin
@termine_blueprint.route("/termine/delete/<int:termin_id>", methods=["POST"])
@login_required
@admin_required
def termine_delete(termin_id):
    form = DeleteTerminForm()
    if not form.validate_on_submit():
        flash("Invalid CSRF token.", "danger")
        return redirect(url_for("termine_blueprint.termine"))

    termin = db.session.query(Termin).filter_by(id=termin_id).first()
    if not termin:
        flash("Termin not found.", "danger")
        return redirect(url_for("termine_blueprint.termine"))

    db.session.delete(termin)
    db.session.commit()
    flash("Termin successfully deleted!", "success")
    return redirect(url_for("termine_blueprint.termine"))

# Route: Claim a Termin (Parent Only)
@termine_blueprint.route("/termine/claim", methods=["POST"])
@login_required
def claim_termin():
    form = DeleteTerminForm()  # For CSRF validation
    if not form.validate_on_submit():
        flash("Invalid CSRF token.", "danger")
        return redirect(url_for("termine_blueprint.termine"))

    termin_id = request.form.get("termin_id")
    termin = db.session.query(Termin).filter_by(id=termin_id).first()

    if not termin:
        flash("Termin not found.", "danger")
        return redirect(url_for("termine_blueprint.termine"))

    if termin.description == "claimed":
        flash("This termin is already claimed.", "warning")
        return redirect(url_for("termine_blueprint.termine"))

    termin.description = "claimed"
    termin.parent_id = current_user.id
    db.session.commit()
    flash("Termin successfully claimed!", "success")
    return redirect(url_for("termine_blueprint.termine"))
