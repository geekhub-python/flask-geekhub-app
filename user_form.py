from wtforms import Form, StringField, SubmitField
from wtforms.validators import Required

class UserForm(Form):
    name = StringField('What is you name?', validators=[Required()])
    submit = SubmitField('Submit')

