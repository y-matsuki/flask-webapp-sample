from flask import Blueprint, render_template, url_for
from flask import abort, request, session, redirect
from jinja2 import TemplateNotFound

from passlib.apps import custom_app_context as pwd_context
from common import db

pages = Blueprint('pages', __name__,
                template_folder='templates')

@pages.route('/', defaults={'page': 'index'})
@pages.route('/<page>')
def show(page):
    try:
        if 'username' in session:
            return render_template('%s.html' % page)
        else:
            return render_template('login.html')
    except TemplateNotFound:
        abort(404)

@pages.route('/user')
@pages.route('/user/<username>')
def user(username=None):
    if 'username' in session:
        users = db.users.find({"username":username})
        for user in users:
            print(user)
            return render_template('user.html', user=user)
        abort(404)

@pages.route('/login', methods=['POST', 'GET'])
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

@pages.route('/logout')
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
