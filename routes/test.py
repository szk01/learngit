from flask import (
    request,
    Blueprint,
    render_template,
    Response,
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

# 传输音频wav文件
@main.route('/audio/<name>')
def audio(name):
    path = '/root/learngit/audio/' + name  # 音频所在的路径

    def gen_audio():                    # 这是一个生成器
        with open(path, 'rb') as wav:
            data = wav.read(1024)
            while data:
                yield data
                log('不断传输1024字节文件...')
                data = wav.read(1024)

    return Response(gen_audio(), mimetype="audio/mpeg3")
