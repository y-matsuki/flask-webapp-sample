import os
from flask import Flask, session
from flask import request, redirect, url_for
from flask import render_template

from flask.ext.session import Session

from pymongo import MongoClient
from blueprint.common import db
from blueprint.pages import pages
from blueprint.home import bp_home
from blueprint.user import bp_user
from blueprint.event import bp_event
from blueprint.comment import bp_comment
from blueprint.point import bp_point

app = Flask(__name__)
app.register_blueprint(pages)
app.register_blueprint(bp_home, url_prefix='/home')
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_event, url_prefix='/event')
app.register_blueprint(bp_comment, url_prefix='/comment')
app.register_blueprint(bp_point, url_prefix='/point')

# SESSION_TYPE = 'mongodb'
# SESSION_PERMANENT = True
# MONGOLAB_URI = os.environ.get('MONGOLAB_URI', None)
# if MONGOLAB_URI:
#     SESSION_MONGODB = MONGOLAB_URI.split('/')[2]
#     SESSION_MONGODB_DB = MONGOLAB_URI.split('/')[3]
#     SESSION_MONGODB_COLLECT = 'sessions'
#     print(MONGOLAB_URI)
#     print(SESSION_MONGODB_DB)
#     print(SESSION_MONGODB_COLLECT)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect('/login')

if __name__ == '__main__':
    app.secret_key = '\x88\xfa\x0c\xaa\xb1%\xb29N\x8b\xd7\n\xdfa6\x1d\xd9a\xcd\xaa\x83\x08\xc1\xef'
    app.run(debug=True,host='0.0.0.0')
