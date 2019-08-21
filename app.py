from flask import (
    Flask,
    request,
)
import requests
from flask_socketio import SocketIO
from utils import log
from routes.index import main as index_routes
from routes.login import main as login_routes, room
from routes.test import main as test_routes
from allFuncs import Funcs
from models.user import db, login_manager
from models import config


# 先要初始化一个 Flask 实例，并将Flask-SocketIO添加到Flask应用程序
app = Flask(__name__)
app.secret_key = 'test for good'
app.config.from_object(config)
db.init_app(app)                        # mysql数据库和app连接

login_manager.init_app(app)              # login_manager模块和app连接

socketio = SocketIO(app)

# 测试蓝图注册
app.register_blueprint(index_routes, url_prefix='/index')
app.register_blueprint(test_routes, url_prefix='/test')
app.register_blueprint(login_routes, url_prefix='/login')


# 给OM服务器发送一个POST请求
def reqestOM(body):
    url = 'https://180.174.1.213:1888/xml'
    payload = body
    headers = {
        'content-type': 'text/xml',
    }
    requests.request("POST", url, data=payload, headers=headers, verify=False)


# 接收客户端发送过来的消息，确认通道连接
@socketio.on('login')
def send(data):
    log('use webScoket receive sucessful', data)
    sid = request.sid                              # io的客户端，用来标识唯一客户端。也是会话id
    pid = data["data"]
    room[pid] = sid
    socketio.emit(event='test_room', data={"message": "test_room"}, room=room.get('215'))

# 发送给指定的客户端

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
    log('测试一下body:', body)
    if body is not None:
        if isinstance(body, str):
            if body == 'ANWSER':                                    # 分机应答
                log('通话建立')
                socketio.emit(event="anwser", data=body)
            else:
                log('发送给OM来电转分机请求')
                reqestOM(body)
        if isinstance(body, dict):
            if body["status"] == "RING":                             # 有电话接入call-in
                log(body["number"])
                socketio.emit(event="ring", data=body)

            elif body["status"] == 'Cdr':                             # 通话结束，发送Cdr话单，包含录音文件的路径
                log('下载的录音网址')
                socketio.emit(event='record', data=body)
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
