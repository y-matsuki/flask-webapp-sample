from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from passlib.apps import custom_app_context as pwd_context

from common import db

import common

bp_user = Blueprint('bp_user', __name__,
                template_folder='templates')

@bp_user.route('')
@bp_user.route('/<username>')
def user(username=None):
    if username == None and 'username' in session:
        users = db.users.find()
        return render_template('users.html', users=users)
    else:
        if session['username'] == username or session['is_admin']:
            users = db.users.find({"username":username})
            for user in users:
                return render_template('user.html', user=user)
        else:
            return redirect('/user')


@bp_user.route('', methods=['POST'])
def add_user():
    if 'username' in session and session['is_admin']:
        if request.form.has_key('username'):
            username = request.form['username']
            if username != '':
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
    if 'username' in session and username != None and username != '':
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


@bp_user.route('/<username>', methods=['DELETE'])
def delete_user(username=None):
    print(username)
    if 'username' in session and username != None:
        user = db.users.find_one({"username":username})
        if user:
            db.users.delete_one(user)
    users = db.users.find()
    return render_template('users.html', users=users)
