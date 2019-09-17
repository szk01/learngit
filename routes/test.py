from flask import (
    request,
    Blueprint,
    render_template,
    Response
)

from utils import log

main = Blueprint('test', __name__)  # 第二个参数指定了该蓝图所在的模块名


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


# 传输图片
@main.route('/images/<name>')
def img_stream(name):
    # path = 'C:/Users/86177/Documents/GitHub/flaskWeb/images/' + name
    path = '/root/learngit/images/' + name
    with open(path, 'rb') as img:
        data = img.read()
        print('传递图片...')
    return data
