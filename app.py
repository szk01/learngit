from flask import (
    Flask,
    request,
)
import requests
from flask_socketio import SocketIO
from utils import log
from routes.index import main as index_routes
from routes.login import main as login_routes
from routes.test import main as test_routes
from allFuncs import Funcs
from models.user import db
from models import config

# 先要初始化一个 Flask 实例，并将Flask-SocketIO添加到Flask应用程序
app = Flask(__name__)
app.secret_key = 'test for good'
app.config.from_object(config)
db.init_app(app)


socketio = SocketIO(app)

# 测试蓝图注册
app.register_blueprint(index_routes, url_prefix='/index')
app.register_blueprint(test_routes, url_prefix='/test')
app.register_blueprint(login_routes, url_prefix='/login')


# 给OM服务器发送一个POST请求
def reqestOM(body):
    url = 'https://180.174.1.213.155:1888/xml'
    payload = body
    headers = {
        'content-type': 'text/xml',
    }
    requests.request("POST", url, data=payload, headers=headers, verify=False)


# 接收客户端发送过来的消息，确认通道连接
@socketio.on('phone')
def send(data):
    log('use webScoket receive sucessful', data)


# 会使用到多线程，不同的进程处理不同的请求
@app.route('/ip_phone', methods=['GET'])
def ip_phone():
    log(request.method)
    xml = request.data  # 传过来的数据类型是byte类型
    xml = xml.decode('utf-8')
    # 开始处理各种请求
    log('OM向应用服务器发送的请求数据:', xml)
    # 将OM的请求数据清洗出来访者id
    funct = Funcs(xml)
    body = funct.funcs()
    log('发送给OM的请求：', body)
    # 接收到一个请求之后，发送一个请求
    # 只要body不为空，说明有请求需要发送。判断一下请求会发送给OM还是js客户端
    if body is not None:
        if '177' in body:
            log(body)
            socketio.emit(event="number", data=body)
        if body == 'phone idle':
            log('分机下线')
            socketio.emit(event="idle", data=body)
        else:
            log('发送来电转分机请求')
            reqestOM(body)
    return 'App Server sucess receive!'


@app.route('/test')
def test():
    return 'test sucess'


# 运行服务器
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        # host='127.0.0.1',
        # local_host='106.15.44.224',
        host='0.0.0.0',
        # host='192.168.101.39',
        port=80,
        app=app,
    )
    socketio.run(**config)
    # app.run() #开始运行服务器
