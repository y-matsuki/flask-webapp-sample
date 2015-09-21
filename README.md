# flask-webapp-sample

- https://devcenter.heroku.com/articles/getting-started-with-python-o

## Run local

```
virtualenv venv
source venv/bin/activate

pip install Flask gunicorn passlib pymongo
pip install Flask gunicorn

heroku local
```

## Deploy

```
heroku login
heroku create
git push heroku master

heroku open
```

## MongoDB

```
heroku addons:create mongolab
```
