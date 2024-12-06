from flask_wtf import FlaskForm
from wtforms.fields.simple import IntegerField
from wtforms import validators


class ElterngespraechTerminDeleteForm(FlaskForm):
    termin_id = IntegerField("termin_id", [validators.InputRequired()])
