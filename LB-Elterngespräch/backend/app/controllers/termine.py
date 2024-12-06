import sqlalchemy
import sqlalchemy.orm

from flask import redirect, request, flash
from flask.templating import render_template
from flask import Blueprint
from forms.ElterngespraechTerminForm import ElterngespraechTerminForm
from forms.ElterngespraechTerminDeleteForm import ElterngespraechTerminDeleteForm
from model.models import ElterngespraechTermine, User, db

termine_blueprint = Blueprint('termine_blueprint', __name__)


@termine_blueprint.route("/termine")
def termine():
    # Session Autocomplete
    session: sqlalchemy.orm.Session = db.session

    # Alle Termine laden
    termine = session.query(ElterngespraechTermine).order_by(ElterngespraechTermine.datum, ElterngespraechTermine.uhrzeit).all()

    return render_template("termine/termine.html", termine=termine)


@termine_blueprint.route("/termine/add", methods=["GET", "POST"])
def termine_add():
    session: sqlalchemy.orm.scoping.scoped_session = db.session

    add_termin_form = ElterngespraechTerminForm()

    # Schüler und Lehrer für Auswahlfeld laden
    users = session.query(User).order_by(User.name).all()
    user_choices = [(user.id, user.name) for user in users]
    add_termin_form.schueler_name.choices = user_choices
    add_termin_form.lehrer_id.choices = user_choices

    if request.method == 'POST':
        if add_termin_form.validate_on_submit():
            new_termin = ElterngespraechTermine()

            new_termin.schueler_name = add_termin_form.schueler_name.data
            new_termin.lehrer_id = add_termin_form.lehrer_id.data
            new_termin.datum = add_termin_form.datum.data
            new_termin.uhrzeit = add_termin_form.uhrzeit.data
            new_termin.dauer_minuten = add_termin_form.dauer_minuten.data
            new_termin.status = add_termin_form.status.data
            new_termin.notizen = add_termin_form.notizen.data
            new_termin.raum = add_termin_form.raum.data

            db.session.add(new_termin)
            db.session.commit()

            return redirect("/termine")
        else:
            return render_template("../templates/termin/termin_add.html", users=users, form=add_termin_form)
    else:
        return render_template("../templates/termin/termin_add.html", users=users, form=add_termin_form)


@termine_blueprint.route("/termine/edit", methods=["GET", "POST"])
def termine_edit():
    session: sqlalchemy.orm.scoping.scoped_session = db.session

    edit_termin_form = ElterngespraechTerminForm()

    # Schüler und Lehrer für Auswahlfeld laden
    users = session.query(User).order_by(User.name).all()
    user_choices = [(user.id, user.name) for user in users]
    edit_termin_form.schueler_name.choices = user_choices
    edit_termin_form.lehrer_id.choices = user_choices

    termin_id = request.args["termin_id"]

    # Termin laden
    termin_to_edit = session.query(ElterngespraechTermine).filter(
        ElterngespraechTermine.termin_id == termin_id).first()

    if request.method == "POST":
        if edit_termin_form.validate_on_submit():
            termin_to_edit.schueler_name = edit_termin_form.schueler_name.data
            termin_to_edit.lehrer_id = edit_termin_form.lehrer_id.data
            termin_to_edit.datum = edit_termin_form.datum.data
            termin_to_edit.uhrzeit = edit_termin_form.uhrzeit.data
            termin_to_edit.dauer_minuten = edit_termin_form.dauer_minuten.data
            termin_to_edit.status = edit_termin_form.status.data
            termin_to_edit.notizen = edit_termin_form.notizen.data
            termin_to_edit.raum = edit_termin_form.raum.data

            db.session.commit()
            return redirect("/termine")
    else:
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
def delete_termin():
    delete_termin_form = ElterngespraechTerminDeleteForm()
    if delete_termin_form.validate_on_submit():
        termin_id_to_delete = delete_termin_form.termin_id.data
        termin_to_delete = db.session.query(ElterngespraechTermine).filter(
            ElterngespraechTermine.termin_id == termin_id_to_delete
        )
        termin_to_delete.delete()
        db.session.commit()
    else:
        print("Fatal Error")

    flash(f"Termin with ID {termin_id_to_delete} has been deleted")

    return redirect("/termine")
