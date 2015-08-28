from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session

from common import db

bp_user = Blueprint('bp_user', __name__)

@bp_user.route('')
@bp_user.route('/<username>')
def user_by_name(username=None):
    if username == None:
        if 'username' in session and session['is_admin']:
            return dumps(db.users.find())
        return jsonify([]), 403
    else:
        if 'username' in session:
            if session['username'] == username or session['is_admin']:
                items = db.users.find({'username':username})
                for item in items:
                    return dumps(item)
                return jsonify({}), 404
        return jsonify({}), 403
