#!/bin/sh
sudo ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
sudo yum install -y git
echo "[MongoDB]
name=MongoDB Repository
baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
gpgcheck=0
enabled=1" | sudo tee -a /etc/yum.repos.d/mongodb.repo
sudo yum install -y mongodb-org-server mongodb-org-shell mongodb-org-tools
sudo service mongod start

sudo pip install flask
sudo pip install pymongo
sudo pip install passlib

python init_mongodb.py
