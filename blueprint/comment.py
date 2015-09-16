# -*- coding: utf-8 -*-
from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime

from common import db

bp_comment = Blueprint('bp_comment', __name__,
                    template_folder='templates')

@bp_comment.route('/<event_id>/<owner>')
def show_comments(event_id=None,owner=None):
    comments = db.comments.find({"event_id":event_id, "owner":owner})
    return render_template('/comments.html', comments=list(comments))

@bp_comment.route('/<event_id>/<owner>/<username>')
def show_comment(event_id=None,owner=None,username=None):
    owner = session['username']
    rating = db.ratings.find_one({"owner":owner,"event_id":event_id,"username":username});
    axes = []
    if rating == None:
        axes = [
            {"name":"theme",       "jp_name": u"お題", "value":3},
            {"name":"authority",   "jp_name": u"説得力", "value":3},
            {"name":"originality", "jp_name": u"独創性", "value":3},
            {"name":"logicality",  "jp_name": u"論理性", "value":3},
            {"name":"time",        "jp_name": u"時間配分", "value":3},
            {"name":"deep",        "jp_name": u"深掘り力", "value":3}
        ]
    else:
        axes = rating['axes']
    print(axes)
    return render_template('comment.html', event_id=event_id, username=username,
                                           axes=axes)


@bp_comment.route('/<event_id>/<username>', methods=['POST'])
def post_comment(event_id=None,username=None):
    if 'username' in session and username != session['username']:
        axes = [
            {"name":"theme",       "jp_name": u"お題", "value": int(request.form['theme'])},
            {"name":"authority",   "jp_name": u"説得力", "value": int(request.form['authority'])},
            {"name":"originality", "jp_name": u"独創性", "value": int(request.form['originality'])},
            {"name":"logicality",  "jp_name": u"論理性", "value": int(request.form['logicality'])},
            {"name":"time",        "jp_name": u"時間配分", "value": int(request.form['time'])},
            {"name":"deep",        "jp_name": u"深掘り力", "value": int(request.form['deeper'])}
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
