from flask import Flask, request, make_response, render_template
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime, timedelta
from user_form import UserForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Geekhub'

Bootstrap(app)
Moment(app)
manager = Manager(app)

@app.route('/')
def index():
    user_agent = get_user_agent()
    return render_template('index.html', browser=user_agent, 
                            date_now=datetime.utcnow())

@app.route('/user/<name>', methods=['GET', 'POST'])
def hello_user(name):
    user_agent = get_user_agent()
    form = UserForm(request.form)
    if request.method == "POST":
        name = form.name.data
        print(name)
    return render_template('user.html', 
                            name=name, user_agent=user_agent, form=form)

@app.route('/redirect')
def redirect():
    return redirect('http://geekhub.ck.ua')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
    
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html', e=e)



def get_user(id):
    return None

def get_user_agent():
    return request.headers.get('User-Agent')



if __name__ == '__main__':
    manager.run()