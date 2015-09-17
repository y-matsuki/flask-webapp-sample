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
        axes = {
            "theme": 3,
            "compel": 3,
            "original": 3,
            "logical": 3,
            "time": 3,
            "deep": 3
        }
    print(axes)
    return render_template('comment.html', event_id=event_id, presenter=presenter,
                                           axes=axes, theme=theme)


@bp_comment.route('/<event_id>/<presenter>', methods=['POST'])
def post_comment(event_id=None,presenter=None):
    if 'username' in session and presenter != session['username']:
        axes = {
            "theme": int(request.form['theme']),
            "compel": int(request.form['compel']),
            "original": int(request.form['original']),
            "logical": int(request.form['logical']),
            "time": int(request.form['time']),
            "deep": int(request.form['deep'])
        }
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
        if request.form.has_key('good') and request.form['good']:
            comment = {
                "type": "good",
                "event_id": event_id,
                "comment": request.form['good'],
                "presenter": presenter
            }
            db.comments.insert(comment);
        if request.form.has_key('bad') and request.form['bad']:
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
    if not ratings:
        return jsonify({ "data": [0, 0, 0, 0, 0, 0] })
    size = len(ratings) * 1.0
    sum_theme, sum_compel, sum_original, sum_logical, sum_time, sum_deep = 0, 0, 0, 0, 0, 0
    for rating in ratings:
        sum_theme += rating['axes']['theme']
        sum_compel += rating['axes']['compel']
        sum_original += rating['axes']['original']
        sum_logical += rating['axes']['logical']
        sum_time += rating['axes']['time']
        sum_deep += rating['axes']['deep']
    item = {
        "data": [
            sum_theme / size,
            sum_compel / size,
            sum_original / size,
            sum_logical / size,
            sum_time / size,
            sum_deep / size
        ]
    }
    return jsonify(item)
