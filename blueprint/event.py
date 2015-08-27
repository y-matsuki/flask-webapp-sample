from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session

from common import db

bp_event = Blueprint('bp_event', __name__,
                    template_folder='templates')

@bp_event.route('/')
def event():
    if 'username' in session:
        return render_template('event.html')
    return redirect(url_for('login'))

@bp_event.route('/api', methods=['POST', 'GET'])
def events():
    if request.method == 'POST':
        request.form['username'],
    else:
        if 'username' in session:
            return dumps(db.events.find())
        return jsonify([]), 403
