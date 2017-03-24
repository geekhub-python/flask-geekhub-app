import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Role, Post


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        post_body = 'Test post!'
        post = Post(body=post_body)
        db.session.add(post)
        db.session.flush()
        response = self.client.get(url_for('main.index'))
        self.assertTrue(b'Stranger' in response.data)
        self.assertTrue(post_body.encode() in response.data)

    def test_register_and_login(self):
        # register a new account
        register_data = {
            'email': 'john@example.com',
            'username': 'john',
            'password': 'cat',
            'password2': 'cat',
            'job': 'test'
        }
        response = self.client.post(url_for('auth.register'), data=register_data)
        self.assertTrue(response.status_code == 302)
        user = User.query.filter_by(email=register_data['email']).first()
        self.assertIsNotNone(user)

        # login with the new account
        response = self.client.post(url_for('auth.login'), data={
            'email': 'john@example.com',
            'password': 'cat'
        }, follow_redirects=True)
        self.assertTrue(re.search(b'Hello,\s+john!', response.data))
        self.assertTrue(
            b'You have not confirmed your account yet' in response.data)

        # send a confirmation token
        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        self.assertTrue(
            b'You have confirmed your account' in response.data)

        # log out
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertTrue(b'You have been logged out' in response.data)
