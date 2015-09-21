import os
from pymongo import MongoClient

MONGOLAB_URI = os.environ.get('MONGOLAB_URI', 'mongodb://localhost:27017/')
print MONGOLAB_URI
client = MongoClient(MONGOLAB_URI)
db  = client.local
