from flask import Flask, session
from flask import request, redirect, url_for
from flask import render_template
from pymongo import MongoClient
from passlib.apps import custom_app_context as pwd_context
from blueprint.common import db
from blueprint.home import bp_home
from blueprint.user import bp_user
from blueprint.event import bp_event

app = Flask(__name__)
app.register_blueprint(bp_home, url_prefix='/home')
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_event, url_prefix='/event')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return redirect('/home')
        else:
            error = 'Invalid username/password'
            return render_template('login.html', error=error)
    else:
        if 'username' in session:
            return redirect('/home')
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('index'))

def valid_login(username, password):
    user = db.users.find_one({"username":username})
    if user == None:
        return False
    if pwd_context.verify(password, user["password"]):
        session['username'] = user['username']
        session['is_admin'] = user['is_admin']
        return True
    return False

if __name__ == '__main__':
    app.secret_key = '\x88\xfa\x0c\xaa\xb1%\xb29N\x8b\xd7\n\xdfa6\x1d\xd9a\xcd\xaa\x83\x08\xc1\xef'
    app.run(debug=True)
