from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session

from common import db

bp_home = Blueprint('bp_home', __name__,
                    template_folder='templates')

@bp_home.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))
