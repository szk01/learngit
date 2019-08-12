from flask import (
    Blueprint
)
from app import app

main = Blueprint('login', __name__)


@main.route('/index', method=['GET'])
def index():
    pass
