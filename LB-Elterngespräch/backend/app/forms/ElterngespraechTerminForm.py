from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, SelectField, StringField, TextAreaField, DateField, TimeField
from wtforms import validators


class ElterngespraechTerminForm(FlaskForm):
    schueler_id = SelectField("Schüler", coerce=int, validators=[validators.InputRequired()])
    lehrer_id = SelectField("Lehrer", coerce=int, validators=[validators.InputRequired()])
    datum = DateField("Datum", format='%Y-%m-%d', validators=[validators.InputRequired()])
    uhrzeit = TimeField("Uhrzeit", format='%H:%M', validators=[validators.InputRequired()])
    dauer_minuten = IntegerField("Dauer (Minuten)", validators=[validators.InputRequired()])
    status = StringField("Status", validators=[validators.Length(max=20), validators.InputRequired()])
    notizen = TextAreaField("Notizen", validators=[validators.Optional()])
    raum = StringField("Raum", validators=[validators.Length(max=50), validators.InputRequired()])
