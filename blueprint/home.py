# -*- coding: utf-8 -*-
from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime
import pymongo, hashlib

from common import db

bp_home = Blueprint('bp_home', __name__,
                    template_folder='templates')

@bp_home.route('')
def home():
    if 'username' in session:
        events = list(db.events.find().sort('date', pymongo.DESCENDING))
        for event in events:
            for theme in event['themes']:
                user = db.users.find_one({"username": theme['username']})
                if user:
                    theme['icon'] = hashlib.md5(user['mailaddr']).hexdigest()
        past_events = []
        next_events = []
        for event in events:
            if event['date'] > datetime.today():
                next_events.append(event)
            else:
                past_events.append(event)
        return render_template('home.html', past_events=past_events,
                                            next_events=next_events)
    else:
        return render_template('login.html')
