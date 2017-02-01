from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):
    name = StringField('What is you name?', validators=[DataRequired(), Length(1, 16)])
    submit = SubmitField('Submit')

