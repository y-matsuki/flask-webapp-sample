# -*- coding: utf-8 -*-
import re
from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime

from common import db

bp_event = Blueprint('bp_event', __name__,
                    template_folder='templates')

@bp_event.route('')
@bp_event.route('/<event_id>')
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


@bp_event.route('', methods=['POST'])
def add_event():
    if 'username' in session and session['is_admin']:
        if request.form.has_key('event_id'):
            event_id = request.form['event_id']
            if re.compile(r'^[0-9A-Za-z-_.]+$').search(event_id) == None:
                events = db.events.find()
                message = 'the event id contains invald character.'
                return render_template('events.html', events=events,
                                                      message=message)
            theme = { "username":"", "title":"" }
            event = {
                "event_id": event_id,
                "title": event_id,
                "date": datetime.utcnow(),
                "themes": [theme.copy(),theme.copy(),theme.copy(),theme.copy()]
            }
            db.events.update_one({"event_id":event_id}, {"$set": event}, upsert=True)
            return redirect('/event/%s' % event_id)
    return redirect('/event')


@bp_event.route('/<event_id>', methods=['POST'])
def update_event(event_id=None):
    if 'username' in session and session['is_admin'] and event_id != None:
        event = db.events.find_one({"event_id":event_id})
        event['title'] = request.form['title']
        event['date'] = datetime.strptime(request.form['date'], "%Y-%m-%d %H:%M:%S.%f")
        themes = []
        for i in xrange(1, 5):
            username, title = "", ""
            if request.form.has_key('username' + str(i)):
                username = request.form['username' + str(i)]
            if request.form.has_key('title' + str(i)):
                title = request.form['title' + str(i)]
            theme = {
                "username": username,
                "title": title
            }
            themes.append(theme)
        event['themes'] = themes
        db.events.update_one({"event_id":event_id}, {"$set": event}, upsert=True)
        return redirect('/event')
    else:
        return redirect('/event')


@bp_event.route('/<event_id>', methods=['DELETE'])
def delete_event(event_id=None):
    if 'username' in session and session['is_admin'] and event_id != None:
        event = db.events.find_one({"event_id":event_id})
        if event:
            db.events.delete_one(event)
    events = db.events.find()
    return render_template('events.html', events=events)
