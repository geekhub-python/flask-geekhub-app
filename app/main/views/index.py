from datetime import datetime

from flask import render_template, request
from .. import main

@main.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return render_template(
        'index.html',
        browser=user_agent,
        date_now=datetime.utcnow()
        )