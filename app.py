from flask import (
    Flask,
)
import time
from flask_socketio import SocketIO
import sys

sys.path.append("/root/learngit/routes/test")  # Linux上加载
import test_bp

# 先要初始化一个 Flask 实例，并将Flask-SocketIO添加到Flask应用程序
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


# 测试蓝图注册
app.register_blueprint(test_bp, url_prefix='/test')


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
    # app.run() 开始运行服务器
