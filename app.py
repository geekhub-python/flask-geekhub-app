from datetime import datetime
import os

from flask import Flask, request, render_template
from flask import redirect, send_from_directory, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from forms.user_form import UserForm
from forms.image_form import ImageUploadForm

from models import db
from models.user import User, Role

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Geekhub'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

Bootstrap(app)
Moment(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

IMAGES_PATH = os.path.join(app.static_folder, 'uploads')


@app.before_request
def before_request():
    """
    docstring
    """
    if 'count' not in session:
        session['count'] = 1
    else:
        session['count'] += 1


@app.after_request
def ar(response):
    response.headers['Test'] = 'hello'
    return response


@app.route('/')
def index():
    user_agent = _get_user_agent()
    return render_template(
        'index.html',
        browser=user_agent,
        date_now=datetime.utcnow()
        )


@app.route('/user', methods=['GET', 'POST'])
def hello_user():
    user_agent = _get_user_agent()

    form = UserForm()
    name = _get_name_from_form(form)

    new = _store_name_in_db_and_return_result(name)
    return render_template('user.html',
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


@app.route('/image', methods=['GET', 'POST'])
def image():
    image = None
    form = ImageUploadForm()
    if form.validate_on_submit():
        image = form.image_file.data.filename
        if not os.path.exists(IMAGES_PATH):
            os.makedirs(IMAGES_PATH)
        form.image_file.data.save(os.path.join(IMAGES_PATH, image))
    return render_template(
        'image.html',
        form=form,
        image='uploads/' + image if image else None
        )


@app.route('/session')
def session_test():
    return render_template('session.html', count=session['count'])


def _get_user_agent():
    return request.headers.get('User-Agent')


@app.route('/redirect')
def geekhub_redirect():
    return redirect('http://geekhub.ck.ua')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def page_error(e):
    return render_template('500.html', e=e)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@manager.command
def seed():
    admin_role = Role(name='Admin')
    user_role = Role(name='User')

    db.session.add(admin_role, user_role)
    db.session.commit()


if __name__ == '__main__':
    db.init_app(app)
    manager.run()
