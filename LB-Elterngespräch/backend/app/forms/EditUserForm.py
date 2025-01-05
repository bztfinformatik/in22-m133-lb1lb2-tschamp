from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class EditUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=150)])
    role = SelectField(
        "Role",
        choices=[("parent", "Parent"), ("teacher", "Teacher"), ("admin", "Admin")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Save Changes")
