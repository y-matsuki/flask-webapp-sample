# -*- coding: utf-8 -*-
from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime

from common import db

bp_comment = Blueprint('bp_comment', __name__,
                    template_folder='templates')


@bp_comment.route('/<event_id>/<presenter>')
def show_comment(event_id=None,presenter=None):
    listener = session['username']
    event = db.events.find_one({"event_id":event_id})
    theme = {}
    for item in event['themes']:
        if presenter == item['username']:
            theme = item
    rating = db.ratings.find_one({
        "event_id":event_id, "presenter":presenter, "listener":listener
    });
    axes = []
    if rating:
        axes = rating['axes']
    else:
        axes = [
            {"name":"theme",       "jp_name": u"お題", "value":3},
            {"name":"authority",   "jp_name": u"説得力", "value":3},
            {"name":"originality", "jp_name": u"独創性", "value":3},
            {"name":"logicality",  "jp_name": u"論理性", "value":3},
            {"name":"time",        "jp_name": u"時間配分", "value":3},
            {"name":"deep",        "jp_name": u"深掘り力", "value":3}
        ]
    return render_template('comment.html', event_id=event_id, presenter=presenter,
                                           axes=axes, theme=theme)


@bp_comment.route('/<event_id>/<presenter>', methods=['POST'])
def post_comment(event_id=None,presenter=None):
    if 'username' in session and presenter != session['username']:
        axes = [
            {"name":"theme",       "jp_name": u"お題", "value": int(request.form['theme'])},
            {"name":"authority",   "jp_name": u"説得力", "value": int(request.form['authority'])},
            {"name":"originality", "jp_name": u"独創性", "value": int(request.form['originality'])},
            {"name":"logicality",  "jp_name": u"論理性", "value": int(request.form['logicality'])},
            {"name":"time",        "jp_name": u"時間配分", "value": int(request.form['time'])},
            {"name":"deep",        "jp_name": u"深掘り力", "value": int(request.form['deep'])}
        ]
        listener = session['username']
        rating = {
            "event_id": event_id,
            "presenter": presenter,
            "axes": axes,
            "listener": listener
        }
        db.ratings.update_one({
            "event_id":event_id, "presenter":presenter, "listener":listener},
            {"$set": rating}, upsert=True)
        if request.form.has_key('good'):
            comment = {
                "type": "good",
                "event_id": event_id,
                "comment": request.form['good'],
                "presenter": presenter
            }
            db.comments.insert(comment);
        if request.form.has_key('bad'):
            comment = {
                "type": "bad",
                "event_id": event_id,
                "comment": request.form['bad'],
                "presenter": presenter
            }
            db.comments.insert(comment);
    return redirect('/home')


@bp_comment.route('/<event_id>')
def show_comments(event_id=None):
    presenter = session['username']
    event = db.events.find_one({"event_id":event_id})
    theme = {}
    for item in event['themes']:
        if presenter == item['username']:
            theme = item
    comments = db.comments.find({"event_id":event_id, "presenter":presenter})
    ratings = db.ratings.find({"event_id":event_id, "presenter":presenter})
    return render_template('/comments.html', comments=list(comments),
                                             theme=theme, rating=len(list(ratings)),
                                             event_id=event_id,presenter=presenter)


@bp_comment.route('/api/<event_id>/<presenter>')
def get_rating(event_id=None,presenter=None):
    ratings = list(db.ratings.find({"event_id":event_id, "presenter":presenter}))
    size = len(ratings) * 1.0
    sum_theme, sum_authority, sum_originality, sum_logicality, sum_time, sum_deep = 0, 0, 0, 0, 0, 0
    for rating in ratings:
        for axe in rating['axes']:
            if axe['name'] == 'theme':
                sum_theme += axe['value']
            elif axe['name'] == 'authority':
                sum_authority += axe['value']
            elif axe['name'] == 'originality':
                sum_originality += axe['value']
            elif axe['name'] == 'logicality':
                sum_logicality += axe['value']
            elif axe['name'] == 'time':
                sum_time += axe['value']
            elif axe['name'] == 'deep':
                sum_deep += axe['value']
    item = {
        "labels": [u"お題", u"説得力", u"独創性", u"論理性", u"時間配分", u"深掘り力"],
        "data": [
            sum_theme / size,
            sum_authority / size,
            sum_originality / size,
            sum_logicality / size,
            sum_time / size,
            sum_deep / size
        ]
    }
    return jsonify(item)
