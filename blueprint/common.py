import os
from pymongo import MongoClient

MONGOLAB_URI = os.environ.get('MONGOLAB_URI', 'mongodb://localhost:27017/local')

client = MongoClient(MONGOLAB_URI)
db  = client.get_default_database()
