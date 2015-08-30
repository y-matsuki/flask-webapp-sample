from flask import Blueprint, render_template, url_for
from flask import abort, request, session, redirect
from jinja2 import TemplateNotFound

from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
from common import db

pages = Blueprint('pages', __name__,
                template_folder='templates')

@pages.route('/')
def show():
    try:
        if 'username' in session:
            return redirect('/home')
        else:
            return render_template('login.html')
    except TemplateNotFound:
        abort(404)

@pages.route('/home')
def home():
    if 'username' in session:
        events = db.events.find()
        past_events = []
        next_events = []
        for event in events:
            if event['date'] > datetime.utcnow():
                next_events.append(event)
            else:
                past_events.append(event)
        return render_template('home.html', past_events=past_events,
                                            next_events=next_events)
    else:
        return render_template('login.html')

@pages.route('/comments/<event_id>/<owner>')
def comments(event_id=None,owner=None):
    comments = db.comments.find({"event_id":event_id, "owner":owner})
    return render_template('/comments.html', comments=list(comments))

@pages.route('/comment/<event_id>/<username>')
def comment(event_id=None,username=None):
    owner = session['username']
    rating = db.ratings.find_one({"owner":owner,"event_id":event_id,"username":username});
    axes = []
    if rating == None:
        axes = [
            {"name":"theme","value":3}, {"name":"authority","value":3},
            {"name":"originality","value":3}, {"name":"logicality","value":3},
            {"name":"time","value":3}, {"name":"deeper","value":3}
        ]
    else:
        axes = rating['axes']
    print(axes)
    return render_template('comment.html', event_id=event_id, username=username,
                                           axes=axes)

@pages.route('/user')
@pages.route('/user/<username>')
def user(username=None):
    if username == None and 'username' in session:
        users = db.users.find()
        return render_template('users.html', users=users)
    else:
        if session['username'] == username or session['is_admin']:
            users = db.users.find({"username":username})
            for user in users:
                return render_template('user.html', user=user)
        else:
            return redirect('/user')


@pages.route('/event')
@pages.route('/event/<event_id>')
def event(event_id=None):
    if event_id == None:
        events = db.events.find()
        return render_template('events.html', events=events)
    else:
        events = db.events.find({"event_id":event_id})
        for event in events:
            users = db.users.find()
            print(event)
            return render_template('event.html', event=event, users=list(users))
        return redirect('/event')

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
        return redirect('/home')

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
