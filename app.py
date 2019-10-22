from flask import (
    Flask,
    request,
    Response,
    session,
)
import requests
from flask_socketio import SocketIO, join_room, leave_room
from utils import log, om_config, wget_down
from routes.index import main as index_routes
from routes.login import main as login_routes
from routes.test import main as test_routes
from routes.client import main as client_routes
from routes.account import main as account_routes
from allFuncs import Funcs
from models.user import db
from models import config
from werkzeug.routing import BaseConverter
from utils import get_phone, auto, getNumber, get_uid
from extension import login_manager
from models.seat import Seat
import random
# 先要初始化一个 Flask 实例，并将Flask-SocketIO添加到Flask应用程序

app = Flask(__name__)
app.secret_key = 'test for good'
app.config.from_object(config)
db.init_app(app)  # mysql数据库和app连接

login_manager.init_app(app)  # login_manager模块和app连接

socketio = SocketIO(app)

# 测试蓝图注册
app.register_blueprint(index_routes, url_prefix='')
app.register_blueprint(test_routes, url_prefix='')
app.register_blueprint(login_routes, url_prefix='')
app.register_blueprint(client_routes, url_prefix='')
app.register_blueprint(account_routes, url_prefix='')


# 注册正则表达式匹配路由
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


# 注册正则表达式
app.url_map.converters['reg'] = RegexConverter

# 传输音频wav文件
@app.route('/audio/<reg("[0-9]{8}"):datatime>/<name>')                   # 解析出两个参数，自动传到方法中
def audio(name, datatime):                                               # 所以方法要接受两个参数
    path = om_config['audio_path'] + name
    def gen_audio():  # 这是一个生成器
        with open(path, 'rb') as wav:
            data = wav.read(1024)
            while data:
                yield data

                data = wav.read(1024)

    log('传输音频文件完成...')
    return Response(gen_audio(), mimetype="audio/mpeg3")

# 钩子函数，任何请求之前，如果没有登录机返回登录页面


# 发送电话会议的请求
def post_om(body):
    body_type = '<?xml version="1.0" encoding="utf-8" ?>\r\n'
    payload = body_type + body
    log('发送呼叫请求', payload)
    url = om_config['om_url']
    requests.request("POST", url, data=payload, verify=False)


# 给OM服务器发送一个POST请求
def reqestOM(body):
    url = om_config['om_url']
    print(url)
    payload = body
    headers = {
        'content-type': 'text/xml',
    }
    requests.request("POST", url, data=payload, headers=headers, verify=False)

# 绑定分机号和io客户端标识,sid
ws = {           # ws的样例

}


# 接收客户端的消息，
@socketio.on('login')
def send(data):
    log('use webScoket receive sucessful', data)
    log('接收到登录信息中的工号', data)
    data = session['number']
    sid = request.sid           # io的客户端，用来标识唯一客户端。也是会话id
    ws[data] = sid
    log('查看ws字典', ws)
    # room = getNumber('213', Seat, ws)           # 213不可以写死
    # socketio.emit(event='test_room', data='connected', room=room)  # 私聊的功能


# 电话会议
@socketio.on('conference')
def conference(data):
    log('接收到%s的数据, 呼叫%s分机' % (data['phone'], data['phone']))
    # 213呼叫号码
    body = '<Transfer attribute="Connect">\r\n<ext id="213"/>\r\n<ext id="%s"/>\r\n</Transfer>' % data['phone']             # 213是写死的
    log(body)
    post_om(body)


# 让第三方进入电话会议
@socketio.on('hold')
def hold(data):
    log('接收到hold', data)
    # 发送212hold请求
    h_body = '<Control attribute="Hold">\r\n<ext id="213"/>\r\n</Control>'
    post_om(h_body)
    # 让第三方会话接入
    t_body = '<Transfer attribute="Connect">\r\n<ext id="213"/>\r\n<ext id="%s"/>\r\n</Transfer>' % data['hphone']
    post_om(t_body)
    # 执行conference命令
    c_body = '<?xml version="1.0" encoding="utf-8" ?><Transfer attribute="Conference"><ext id="213"/></Transfer>'
    post_om(c_body)


# 触发满意度评价
@socketio.on('satisfy')                     # 接收到消息转到语音播报
def satisfy(data):
    log('接收到点击按钮传递的信息', data)
    # 发送语音评价
    s_body = '<Transfer attribute="Connect"><visitor id="%s" /><menu id="1"/></Transfer>' % ws['tran_id']
    log('转发到语音播报命令', s_body)
    post_om(s_body)

# 存储来电转分机的分机号
setting_phone = {
    'pid': None,
}

# 设置分机的优先级
@socketio.on('priority')
def setting_priority(data):
    log('接收到设置优先级', data)
    priori = {}
    priori['priority'] = data
    Funcs.p.update(priori)                          # 前端发送过来的优先级设置，更新到allFuncs中的分机设置
    log('前台页面想要设置的分机优先级：', Funcs.p)
    set_phone = get_phone(data, Funcs.p)            # 拿到优先级最高的分机
    log('能得到的分机是', set_phone)
    if set_phone:
        setting_phone['pid'] = set_phone
    else:
        log('分机优先级设置失败')



# 处理各种不同的body
def extcute_body(body):
    if isinstance(body, dict):

        if body.get("status") == "RING":  # 有电话接入call-in，客户端显示页面
            log(body["number"])
            log('有电话接入，显示弹窗')
            ws['tran_id'] = body['vid']  # 将来访者id写入ws字典，供满意度调查按钮使用
            seatId = body['pid']                        # seatId是分机号
            room = getNumber(seatId, Seat, ws)
            if room is not None:                        # 如果相应的账号登录
                socketio.emit(event='ring', data=body, room=room)

        elif isinstance(body.get('ws'), dict):
            log('通话结束传过来的body', body)
            if body['ws']['status'] == 'Cdr':
                # 通话结束，发送Cdr话单，包含录音文件的路径
                log('通话结束，停止计时')
                seatId = body['ws']['pid']
                room = getNumber(seatId, Seat, ws)
                uid = get_uid(Seat, int(seatId))
                log('得到用户id', uid)
                Funcs.sql_addCallRecord(body['cr'], uid)                 # 添加通话记录
                Funcs.sql_addVoiceRecord(body['vr'], uid)                 # 添加录音记录
                socketio.emit(event='off', data=body['ws'], room=room)
                wget_down(body['ws']['downPath'])                     # 下载录音

        elif body.get("status") == 'ANWSER':  # 分机应答，让计时器开始计时
            log('通话建立')
            seatId = body['pid']
            room = getNumber(seatId, Seat, ws)
            socketio.emit(event='anwser', data=body, room=room)

        elif body.get("status") == 'Transfer':              # 来电转分机请求
            log('发送来电转分机请求')
            ws['tran_id'] = body['vid']             # 将来访者id写入ws字典，供满意度调查按钮使用
            if setting_phone['pid']:                # 如果设置分机的优先级，使用优先分机
                auto(body['vid'], setting_phone['pid'])
            else:
                pid = list(Funcs.p['IDLE'])             # 如果没有设置分机的优先机，就使用allFunc中的写死的默认分机213
                #auto(body['vid'], pid[0])
                auto(body['vid'], random.choice(pid))
                #auto(body['vid'], '269')                    # 指定分机

        elif body.get("status") == 'change_status':         # 分机状态改变
            socketio.emit(event='phone_status', data=body)              # 广播给所有客户端，显示分机的状态


# 接收OM的消息
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
        extcute_body(body)
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
