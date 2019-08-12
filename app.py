from flask import (
    Flask,
)
from flask_socketio import SocketIO

from routes.login import main
from routes.OM import *
from routes.index import bp as todo_login
from routes.test import *

import requests
import time
from multiprocessing import Pool
from allFuncs import Funcs

# 先要初始化一个 Flask 实例，并将Flask-SocketIO添加到Flask应用程序
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


# 用 log 函数把所有输出写入到文件，这样就能很方便地掌控全局了
# 即便你关掉程序，也能再次打开来查看，这就是个时光机
def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


# 测试蓝图注册
app.register_blueprint(bp, url_prefix='/test')
app.register_blueprint(main, url_prefix='/index')
app.register_blueprint(main, url_prefix='/OM')
app.register_blueprint(todo_login, url_prefix='/login')


# 接收客户端发送过来的消息
@socketio.on('login')
def test_message(data):
    log('服务端接收的消息成功', data)


# 运行服务器
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        # debug=True,
        host='0.0.0.0',
        # local_host='106.15.44.224',
        # om_host='180.175.33.122',
        # host='192.168.101.39',
        port=80,
        app=app,
    )
    socketio.run(**config)
    # socketio.run(app)                   #socket添加到flask上
    # app.run() 开始运行服务器
    # 所以你访问下面的网址就可以打开网站了
    # http://127.0.0.1:2000/
