#!/bin/sh
cd `dirname $0`

# Setup
mkdir -p data/mongo_test
mongod\
 --dbpath data/mongo_test\
 --fork\
 --logpath data/mongo.log\
 --pidfilepath `pwd`/data/mongo.pid

# Init Database
python scripts/init_mongo.py

# Testing
python test.py

# Teardown
kill `cat data/mongo.pid`
rm -rf data/mongo_test
rm data/mongo.log*
rm data/mongo.pid*
