import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from app.models import User, Role, Post

from app import create_app, db

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)


@manager.command
def seed(Role=Role):
    Role.insert_roles()


@manager.command
def generate_fake():
    from random import seed, randint
    import forgery_py
    from sqlalchemy.exc import IntegrityError
    COUNT = 100

    seed()
    for i in range(COUNT):
        u = User(email=forgery_py.internet.email_address(),
                 username=forgery_py.internet.user_name(True),
                 password="password",
                 confirmed=True,
                 name=forgery_py.name.full_name(),
                 location=forgery_py.address.city(),
                 about_me=forgery_py.lorem_ipsum.sentence(),
                 member_since=forgery_py.date.date(True))
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    seed()
    user_count = User.query.count()
    for i in range(COUNT):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                 timestamp=forgery_py.date.date(True),
                 author=u)
        db.session.add(p)
        db.session.commit()


@manager.command
@manager.option('-t')
def test(test=None):
    """Run the unit tests."""
    import unittest
    if test:
        tests = unittest.TestLoader().discover('tests', pattern=test)
    else:
        tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    unittest.TextTestRunner(verbosity=2).run(tests)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
