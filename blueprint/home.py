from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime

from common import db

bp_home = Blueprint('bp_home', __name__,
                    template_folder='templates')

@bp_home.route('')
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
