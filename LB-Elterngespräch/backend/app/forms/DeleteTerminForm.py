# forms/DeleteTerminForm.py
from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired

class DeleteTerminForm(FlaskForm):
    csrf_token = HiddenField(validators=[DataRequired()])
