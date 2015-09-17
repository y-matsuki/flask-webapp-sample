#!/bin/sh
sudo ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
sudo yum install -y git

# mongodb
echo "[MongoDB]
name=MongoDB Repository
baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
gpgcheck=0
enabled=1" | sudo tee -a /etc/yum.repos.d/mongodb.repo
sudo yum install -y mongodb-org-server mongodb-org-shell mongodb-org-tools
sudo service mongod start

# prepare for python application
sudo pip install flask
sudo pip install pymongo
sudo pip install passlib

# insert initial data
git clone https://github.com/y-matsuki/flask-webapp-sample.git
cd flask-webapp-sample
python scripts/init_mongodb.py

# reverse proxy
sudo yum install -y nginx
sudo rm /etc/nginx/conf.d/reco-study.conf
echo "server {
    listen 80;
    location / {
        proxy_pass http://localhost:5000;
    }
}" | sudo tee -a /etc/nginx/conf.d/reco-study.conf
sudo service nginx restart
