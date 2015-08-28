from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from passlib.apps import custom_app_context as pwd_context

from common import db

bp_user = Blueprint('bp_user', __name__)

@bp_user.route('', methods=['GET'])
@bp_user.route('/<username>', methods=['GET'])
def get_user(username=None):
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

@bp_user.route('', methods=['POST'])
def add_user():
    print('AAA')
    if 'username' in session and session['is_admin']:
        if request.form.has_key('username'):
            print 'BBB: ', request.form['username']
            username = request.form['username']
            user = {
                "username": username,
                "password": pwd_context.encrypt("password"),
                "mailaddr": "user@example.com",
                "is_admin": False
            }
            db.users.update_one({"username":username}, {"$set": user}, upsert=True)
            return redirect('/user/%s' % username)
    return redirect('/user')

@bp_user.route('/<username>', methods=['POST'])
def update_user(username=None):
    if 'username' in session and username != None:
        user = db.users.find_one({"username":username})
        user['username'] = request.form['username']
        if request.form['password'] != user['password']:
            user['password'] = pwd_context.encrypt(request.form['password'])
        user['mailaddr'] = request.form['mailaddr']
        if request.form.has_key('is_admin'):
            user['is_admin'] = True
        else:
            user['is_admin'] = False
        db.users.update_one({"username":username}, {"$set": user}, upsert=True)
    return redirect('/user')
