# flask-webapp-sample

- https://devcenter.heroku.com/articles/getting-started-with-python-o

## Run local

```
mongod --dbpath data/mongo

virtualenv venv
source venv/bin/activate

pip install Flask Flask-Sessions gunicorn passlib pymongo

heroku local
```

## Deploy to heroku

```
heroku login
heroku create
git push heroku master

heroku open
```

## MongoDB

```
heroku addons:create mongolab
heroku run python scripts/init_mongo.py
```
