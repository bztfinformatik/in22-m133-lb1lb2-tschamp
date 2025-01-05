from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class ElterngespraechTerminForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description", validators=[Length(max=500)])
    date = DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField("Time", format='%H:%M', validators=[DataRequired()])
