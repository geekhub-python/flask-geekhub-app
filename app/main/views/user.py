from flask import render_template, request

from app import db
from app.models.user import User
from .. import main
from ..forms.user_form import UserForm

@main.route('/user', methods=['GET', 'POST'])
def hello_user():
    user_agent = _get_user_agent()

    form = UserForm()
    name = _get_name_from_form(form)

    new = _store_name_in_db_and_return_result(name)
    return render_template('main/user.html',
                           name=name,
                           user_agent=user_agent,
                           form=form,
                           new=new)

def _get_name_from_form(form):
    if not form.validate_on_submit():
        return None

    name = form.name.data
    form.name.data = ''

    return name


def _store_name_in_db_and_return_result(name):
    if User.query.filter_by(name=name).first():
        return None

    db.session.add(User(name=name))
    db.session.commit()

    return True

def _get_user_agent():
    return request.headers.get('User-Agent')