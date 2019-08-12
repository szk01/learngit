from flask import (
    request,
    render_template,
    Blueprint
)

from app import log

test_bp = Blueprint('test', __name__)       # 第二个参数指定了该蓝图所在的模块名


@test_bp.route('/testPhone', methods=['GET'])
def test_connect():
    method = request.method
    data = request.data
    log('请求方法：', method)
    log('数据：\n', data)
    return 'test connect sucess! SZFY'

# 使用webSocket协议，连接应用服务器和浏览器web
@test_bp.route('/testWeb')
def index():
    return render_template('test.html')
