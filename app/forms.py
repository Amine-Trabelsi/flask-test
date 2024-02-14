from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    balance = FloatField('Balance', validators=[DataRequired()])
    submit = SubmitField('Submit')