from datetime import datetime
import os

from flask import Flask, request, render_template, redirect, send_from_directory, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager

from forms.user_form import UserForm
from forms.image_form import ImageUploadForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Geekhub'

Bootstrap(app)
Moment(app)
manager = Manager(app)

IMAGES_PATH = os.path.join(app.static_folder, 'uploads')

@app.route('/')
def index():
    user_agent = _get_user_agent()
    return render_template('index.html', browser=user_agent, date_now=datetime.utcnow())


@app.route('/user', methods=['GET', 'POST'])
def hello_user():
    name = None
    user_agent = _get_user_agent()

    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('user.html', name=name, user_agent=user_agent, form=form)

@app.route('/image', methods=['GET', 'POST'])
def image():
    image = None
    form = ImageUploadForm()
    if form.validate_on_submit():
        image = form.image_file.data.filename
        if not os.path.exists(IMAGES_PATH):
            os.makedirs(IMAGES_PATH)
        form.image_file.data.save(os.path.join(IMAGES_PATH, image))
    return render_template('image.html', form=form, image='uploads/' + image if image else None)

@app.route('/session')
def session_test():
    if 'count' not in session:
        session['count'] = 1
    else:
        session['count'] += 1
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
def page_not_found(e):
    return render_template('500.html', e=e)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    manager.run()