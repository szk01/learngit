from flask import (
    Blueprint
)
from app import app

bp = Blueprint('login', __name__)


@bp.route('/index', method=['GET'])
def index():
    pass
