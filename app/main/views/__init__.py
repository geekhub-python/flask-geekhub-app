from flask import session, current_app as app, send_from_directory
import os
from .. import main

from .images import *
from .index import *
from .user import *

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
