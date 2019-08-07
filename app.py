from flask import (
    Flask,
    request,
    render_template,
)
from flask_socketio import SocketIO,emit

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


#给OM服务器发送一个POST请求
def reqestOM(body):
    url = 'https://zhidi.sfyf.cn:1888/xml'
    payload = body
    headers = {
        'content-type':'text/xml',
    }
    requests.request("POST", url, data=payload, headers=headers, verify=False)


@app.route('/testPhone', methods=['GET'])
def test_connect():
    method = request.method
    data = request.data
    log('请求方法：',method)
    log('数据：\n',data)
    return 'test connect sucess! SZFY'


#会使用到多线程，不同的进程处理不同的请求
@app.route('/ip_phone', methods=['GET'])
def ip_phone():
    log(request.method)
    xml = request.data              #传过来的数据类型是byte类型
    xml = xml.decode('utf-8')
    #开始处理各种请求
    log('OM向应用服务器发送的请求数据:', xml)
        #将OM的请求数据清洗出来访者id
    funct = Funcs(xml)
    body = funct.funcs()
    log('发送给OM的请求：', body)
        #接收到一个请求之后，发送一个请求
            #只要body不为空，说明有请求需要发送
    if body != None:
        reqestOM(body)
    return 'App Server sucess receive!'


#使用webSocket协议，连接应用服务器和浏览器web
@app.route('/testWebSocket')
def index():
    return render_template('test.html')


@socketio.on('my event', namespace='/testWebSocket')
def test_message():
    emit('server_response',
         {'data':"连接webSocket成功"})        #emit()函数中有两个参数




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
