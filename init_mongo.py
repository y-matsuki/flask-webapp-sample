from pymongo import MongoClient
from bson.json_util import dumps
from passlib.apps import custom_app_context as pwd_context

client = MongoClient('localhost', 27017)
db  = client.local
users = db.users

f = open('data/users.csv')
lines = f.readlines()
f.close()

for line in lines:
    username = line.strip().split(',')[1]
    user = users.find_one({"username":username})
    password = None
    if user != None:
        password = user['password']
    else:
        password = pwd_context.encrypt(line.strip().split(',')[2])
    user = {
        'is_admin': line.strip().split(',')[0],
        'username': username,
        'password': password,
        'mailaddr': line.strip().split(',')[3]
    }
    users.update_one({"username":username}, {"$set": user}, upsert=True)
