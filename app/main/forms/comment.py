from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(Form):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')