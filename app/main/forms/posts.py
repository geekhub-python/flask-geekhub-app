from flask_wtf import Form
from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')