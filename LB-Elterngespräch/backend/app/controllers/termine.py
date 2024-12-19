from flask import redirect, request, flash, render_template, Blueprint
from flask_login import login_required, current_user
from forms.ElterngespraechTerminForm import ElterngespraechTerminForm
from forms.ElterngespraechTerminDeleteForm import ElterngespraechTerminDeleteForm
from model.models import ElterngespraechTermine, User, db
from functools import wraps

termine_blueprint = Blueprint('termine_blueprint', __name__)

# Restrict access to admin users
"""
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash("You do not have permission to access this page.", "danger")
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function
"""

@termine_blueprint.route("/termine")
@login_required
#@admin_required
def termine():
    session = db.session
    termine = session.query(ElterngespraechTermine).order_by(ElterngespraechTermine.datum, ElterngespraechTermine.uhrzeit).all()
    return render_template("termin/termine.html", termine=termine)

@termine_blueprint.route("/termine/add", methods=["GET", "POST"])
@login_required
#@admin_required
def termine_add():
    session = db.session
    add_termin_form = ElterngespraechTerminForm()
    users = session.query(User).order_by(User.username).all()
    user_choices = [(user.id, user.username) for user in users]
    add_termin_form.schueler_name.choices = user_choices
    add_termin_form.lehrer_id.choices = user_choices

    if request.method == 'POST':
        if add_termin_form.validate_on_submit():
            new_termin = ElterngespraechTermine(
                schueler_name=add_termin_form.schueler_name.data,
                lehrer_id=add_termin_form.lehrer_id.data,
                datum=add_termin_form.datum.data,
                uhrzeit=add_termin_form.uhrzeit.data,
                dauer_minuten=add_termin_form.dauer_minuten.data,
                status=add_termin_form.status.data,
                notizen=add_termin_form.notizen.data,
                raum=add_termin_form.raum.data
            )
            db.session.add(new_termin)
            db.session.commit()
            flash("Termin added successfully!", "success")
            return redirect("/termine")
    return render_template("../templates/termin/termin_add.html", users=users, form=add_termin_form)

@termine_blueprint.route("/termine/edit", methods=["GET", "POST"])
@login_required
#@admin_required
def termine_edit():
    session = db.session
    edit_termin_form = ElterngespraechTerminForm()
    users = session.query(User).order_by(User.username).all()
    user_choices = [(user.id, user.username) for user in users]
    edit_termin_form.schueler_name.choices = user_choices
    edit_termin_form.lehrer_id.choices = user_choices

    termin_id = request.args.get("termin_id")
    termin_to_edit = session.query(ElterngespraechTermine).filter_by(termin_id=termin_id).first()

    if not termin_to_edit:
        flash("Termin not found.", "danger")
        return redirect("/termine")

    if request.method == "POST" and edit_termin_form.validate_on_submit():
        termin_to_edit.schueler_name = edit_termin_form.schueler_name.data
        termin_to_edit.lehrer_id = edit_termin_form.lehrer_id.data
        termin_to_edit.datum = edit_termin_form.datum.data
        termin_to_edit.uhrzeit = edit_termin_form.uhrzeit.data
        termin_to_edit.dauer_minuten = edit_termin_form.dauer_minuten.data
        termin_to_edit.status = edit_termin_form.status.data
        termin_to_edit.notizen = edit_termin_form.notizen.data
        termin_to_edit.raum = edit_termin_form.raum.data

        db.session.commit()
        flash("Termin updated successfully!", "success")
        return redirect("/termine")

    edit_termin_form.schueler_name.data = termin_to_edit.schueler_name
    edit_termin_form.lehrer_id.data = termin_to_edit.lehrer_id
    edit_termin_form.datum.data = termin_to_edit.datum
    edit_termin_form.uhrzeit.data = termin_to_edit.uhrzeit
    edit_termin_form.dauer_minuten.data = termin_to_edit.dauer_minuten
    edit_termin_form.status.data = termin_to_edit.status
    edit_termin_form.notizen.data = termin_to_edit.notizen
    edit_termin_form.raum.data = termin_to_edit.raum

    return render_template("termine/termine_edit.html", users=users, form=edit_termin_form)

@termine_blueprint.route("/termine/delete", methods=["POST"])
@login_required
#@admin_required
def delete_termin():
    delete_termin_form = ElterngespraechTerminDeleteForm()
    if delete_termin_form.validate_on_submit():
        termin_id_to_delete = delete_termin_form.termin_id.data
        termin_to_delete = db.session.query(ElterngespraechTermine).filter_by(termin_id=termin_id_to_delete).first()
        if termin_to_delete:
            db.session.delete(termin_to_delete)
            db.session.commit()
            flash(f"Termin with ID {termin_id_to_delete} has been deleted.", "success")
        else:
            flash("Termin not found.", "danger")
    return redirect("/termine")

@termine_blueprint.route("/termine/claim", methods=["POST"])
@login_required
def claim_termin():
    session = db.session
    termin_id = request.form.get("termin_id")
    
    # Find the specified appointment
    termin_to_claim = session.query(ElterngespraechTermine).filter_by(termin_id=termin_id).first()

    if not termin_to_claim:
        flash("Termin not found.", "danger")
        return redirect("/termine")

    if termin_to_claim.status == "claimed":
        flash("This termin is already claimed.", "warning")
        return redirect("/termine")

    # Update the status and assign the current user as the claimer
    termin_to_claim.status = "claimed"
    termin_to_claim.schueler_name = current_user.id  # Assuming current_user.id is the user's unique identifier
    
    session.commit()
    flash(f"Termin {termin_id} has been successfully claimed!", "success")
    return redirect("/termine")

