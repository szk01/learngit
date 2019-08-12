from flask import (
    request,
    render_template,
    Blueprint
)

from app import log

main = Blueprint('test', __name__)


@main.route('/testPhone', methods=['GET'])
def test_connect():
    method = request.method
    data = request.data
    log('请求方法：', method)
    log('数据：\n', data)
    return 'test connect sucess! SZFY'


