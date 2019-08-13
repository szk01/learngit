from flask import (
    request,
    Blueprint,
    render_template,
)

from utils import log

main = Blueprint('test', __name__)       # 第二个参数指定了该蓝图所在的模块名


@main.route('/testPhone', methods=['GET'])
def test_connect():
    method = request.method
    data = request.data
    log('请求方法：', method)
    log('数据：\n', data)
    return '<h2>test connect sucess! SZFY</h2>'

# 使用webSocket协议，连接应用服务器和浏览器web
@main.route('/testWeb')
def index():
    return render_template('test.html')
