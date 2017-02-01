from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length

class UserForm(Form):
    name = StringField('What is you name?', validators=[Required(), 
                                                        Length(1, 16)])
    submit = SubmitField('Submit')

