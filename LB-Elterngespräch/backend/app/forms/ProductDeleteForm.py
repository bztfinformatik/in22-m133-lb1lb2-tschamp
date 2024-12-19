from flask_wtf import FlaskForm
from wtforms import StringField, validators
from flask_wtf import FlaskForm



class ProductDeleteForm(FlaskForm):
    productCode = StringField("productCode", [validators.InputRequired()])
