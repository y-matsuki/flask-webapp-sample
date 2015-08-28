from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session

from common import db

bp_event = Blueprint('bp_event', __name__,
                    template_folder='templates')

@bp_event.route('', methods=['GET'])
@bp_event.route('/<date>', methods=['GET'])
def get_events(date=None):
    if event_id == None:
        if 'username' in session and session['is_admin']:
            return dumps(db.events.find())
        return jsonify([]), 403
    else:
        if 'username' in session:
            return dumps(db.events.find({'date':date}))
        return jsonify({}), 403


@bp_event.route('', methods=['POST'])
@bp_event.route('/<date>', methods=['POST'])
def post_events(date=None):
    if 'username' in session and session['is_admin']:
        event = {}
        if date != None:
            event = db.events.find({'date':date})
        event['tite'] = request.form['title']
        event['date'] = request.form['date'],
        event['start_time'] = request.form['start_time']
        event['end_time'] = request.form['end_time']
        db.users.update_one({"date":event['date']}, {"$set": event}, upsert=True)
    return jsonify({}), 403
