import os
from pymongo import MongoClient
from bson.json_util import dumps
from passlib.apps import custom_app_context as pwd_context

MONGOLAB_URI = os.environ.get('MONGOLAB_URI', 'mongodb://localhost:27017/')

client = MongoClient(MONGOLAB_URI)
db  = client.local

f = open('data/users.csv')
lines = f.readlines()
f.close()

for line in lines:
    username = line.strip().split(',')[1]
    user = db.users.find_one({"username":username})
    is_admin = False
    if line.strip().split(',')[0] == '1':
        is_admin = True
    password = None
    if user != None:
        password = user['password']
    else:
        password = pwd_context.encrypt(line.strip().split(',')[2])
    user = {
        'is_admin': is_admin,
        'username': username,
        'password': password,
        'mailaddr': line.strip().split(',')[3]
    }
    db.users.update_one({"username":username}, {"$set": user}, upsert=True)
