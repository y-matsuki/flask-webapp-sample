from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

api = Blueprint('api', __name__)

@api.route('/hoge')
def hoge():
    return 'hogehoge'
