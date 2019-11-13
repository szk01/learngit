from flask import (
    request,
    Blueprint,
    render_template,
    Response
)

from utils import log, om_config


main = Blueprint('binary', __name__)          # 第二个参数指定了该蓝图所在的模块名


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
    return render_template('note.html')


# 传输图片
@main.route('/images/<name>')
def img_stream(name):
    path = om_config['img_path'] + name
    with open(path, 'rb') as img:
        data = img.read()
        print('传递图片...')
    return data


# # 传输音频wav文件
# @main.route('/audio/<reg("[0-9]{8}"):datatime>/<name>')  # 解析出两个参数，自动传到方法中
# def audio(name, datatime):  # 所以方法要接受两个参数
#
#     path = om_config['audio_path'] + name
#
#     def gen_audio():  # 这是一个生成器
#         with open(path, 'rb') as wav:
#             data = wav.read(1024)
#             while data:
#                 yield data
#
#                 data = wav.read(1024)
#
#     log('传输音频文件完成...')
#     return Response(gen_audio(), mimetype="audio/mpeg3")
