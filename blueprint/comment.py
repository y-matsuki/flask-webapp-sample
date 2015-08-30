from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime

from common import db

bp_comment = Blueprint('bp_comment', __name__,
                    template_folder='templates')


@bp_comment.route('/<event_id>/<username>', methods=['POST'])
def update_event(event_id=None,username=None):
    if 'username' in session and username != session['username']:
        axes = [
            {"name":"theme",       "value": int(request.form['theme'])},
            {"name":"authority",   "value": int(request.form['authority'])},
            {"name":"originality", "value": int(request.form['originality'])},
            {"name":"logicality",  "value": int(request.form['logicality'])},
            {"name":"time",        "value": int(request.form['time'])},
            {"name":"deeper",      "value": int(request.form['deeper'])}
        ]
        rating = {
            "event_id": event_id,
            "username": username,
            "axes": axes,
            "owner": session['username']
        }
        db.ratings.update_one({"event_id":event_id,"username":username},
                              {"$set": rating}, upsert=True)
        if request.form.has_key('good'):
            comment = {
                "type": "good",
                "event_id": event_id,
                "comment": request.form['good'],
                "owner": username
            }
            db.comments.insert(comment);
        if request.form.has_key('bad'):
            comment = {
                "type": "bad",
                "event_id": event_id,
                "comment": request.form['bad'],
                "owner": username
            }
            db.comments.insert(comment);
    return redirect('/home')
