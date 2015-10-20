# -*- coding: utf-8 -*-
import json
from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime

from common import db

bp_point = Blueprint('bp_point', __name__,
                    template_folder='templates')

@bp_point.route('/api/<event_id>/<presenter>/<type>')
def get_point(event_id=None,presenter=None,type=None):
    if 'username' in session:
        count = db.points.find_one(
            {"event_id":event_id,"presenter":presenter,"type":type})
        if count:
            return jsonify(json.loads(dumps(count)))
    return jsonify({ "count": 0 })


@bp_point.route('/api/<event_id>/<presenter>/<type>', methods=['POST'])
def increment_point(event_id=None,presenter=None,type=None):
    if 'username' in session:
        point = db.points.update(
            {"event_id":event_id,"presenter":presenter,"type":type},
            {'$inc': {'count': 1}}, upsert=True)
        count = db.points.find_one(
            {"event_id":event_id,"presenter":presenter,"type":type})
        return jsonify(json.loads(dumps(count)))
    return jsonify({ "count": 0 })
