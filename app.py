from flask import (
    Flask,
    request,
)

import time
import json
import xml.dom.minidom as xmldom
from multiprocessing import Pool
from allFuncs import Funcs
# 先要初始化一个 Flask 实例
app = Flask(__name__)

# message_list 用来存储所有的 message
message_list = []

# 用 log 函数把所有输出写入到文件，这样就能很方便地掌控全局了
# 即便你关掉程序，也能再次打开来查看，这就是个时光机
def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


@app.route('/test', methods=['GET'])
def test_connect():
    method = request.method
    data = request.data
    log('请求方法：',method)
    log('数据：\n',data)
    return 'test connect sucess! SZFY'


@app.route('/ip_phone', methods=['GET'])
def ip_phone():
    log(request.method)
    xml = request.data              #传过来的数据类型是byte类型
    xml = xml.decode('utf-8')
    #开始处理各种请求
    log('请求类型：',type(xml))
    log('请求数据:', xml)
    funct = Funcs(xml)
    res = funct.funcs()
    log('返回的数据：', res)
    return res




# 运行服务器
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        # debug=True,
        host='0.0.0.0',
        # host='192.168.101.39',
        port=80,
    )
    app.run(**config)
    # app.run() 开始运行服务器
    # 所以你访问下面的网址就可以打开网站了
    # http://127.0.0.1:2000/
