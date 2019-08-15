from flask import (
    Blueprint,
)


main = Blueprint('index', __name__)


@main.route('/index', methods=['GET'])
def index():
    return '成功'