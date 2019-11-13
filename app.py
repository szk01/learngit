from flask import (
    Flask,
    request,
    Response,
)

from Socket.scoket import socketio, ws, setting_phone
from utils import log, om_config, wget_down
from routes.index import main as index_routes
from routes.login import main as login_routes
from routes.binary import main as binary_routes
from routes.client import main as client_routes
from routes.account import main as account_routes
from routes.ccompany import main as ccompany_routes
from routes.power import main as power_routes
from allFuncs import Funcs
from models.user import db
from models import config
from werkzeug.routing import BaseConverter
from utils import get_phone, auto, getNumber, get_uid
from extension import login_manager
from models.seat import Seat
from features.shortMessage import send_message
from features.test_welcome import welcome


app = Flask(__name__)
app.secret_key = 'test for good'
app.config.from_object(config)
db.init_app(app)  # mysql数据库和app连接

login_manager.init_app(app)  # login_manager模块和app连接

socketio.init_app(app)

# 测试蓝图注册
app.register_blueprint(index_routes, url_prefix='')
app.register_blueprint(binary_routes, url_prefix='')
app.register_blueprint(login_routes, url_prefix='')
app.register_blueprint(client_routes, url_prefix='')
app.register_blueprint(account_routes, url_prefix='')
app.register_blueprint(ccompany_routes, url_prefix='')
app.register_blueprint(power_routes, url_prefix='')


# 注册正则表达式匹配路由
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


# 注册正则表达式
app.url_map.converters['reg'] = RegexConverter


# 传输音频wav文件
@app.route('/audio/<reg("[0-9]{8}"):datatime>/<name>')  # 解析出两个参数，自动传到方法中
def audio(name, datatime):  # 所以方法要接受两个参数

    path = om_config['audio_path'] + name

    def gen_audio():  # 这是一个生成器
        with open(path, 'rb') as wav:
            data = wav.read(1024)
            while data:
                yield data

                data = wav.read(1024)

    log('传输音频文件完成...')
    return Response(gen_audio(), mimetype="audio/mpeg3")


# 处理各种不同的body
def extcute_body(body):
    if isinstance(body, dict):

        if body.get("status") == "RING":  # 有电话接入call-in，客户端显示页面
            log(body["number"])
            log('有电话接入，显示弹窗')
            ws['tran_id'] = body['vid']  # 将来访者id写入ws字典，供满意度调查按钮使用
            seatId = body['pid']  # seatId是分机号
            room = getNumber(seatId, Seat, ws)
            socketio.emit(event='ring', data=body, room=room)

        elif isinstance(body.get('ws'), dict):
            log('通话结束传过来的body', body)
            if body['ws']['status'] == 'Cdr':
                # 通话结束，发送Cdr话单，包含录音文件的路径
                log('通话结束，停止计时')
                seatId = body['ws']['pid']
                room = getNumber(seatId, Seat, ws)
                uid = get_uid(Seat, int(seatId))
                Funcs.sql_addCallRecord(body['cr'], uid)  # 添加通话记录
                Funcs.sql_addVoiceRecord(body['vr'], uid)  # 添加录音记录
                socketio.emit(event='off', data=body['ws'], room=room)
                wget_down(body['ws']['downPath'])  # 下载录音

        elif body.get("status") == 'ANWSER':  # 分机应答，让计时器开始计时
            log('通话建立')
            seatId = body['pid']
            room = getNumber(seatId, Seat, ws)
            socketio.emit(event='anwser', data=body, room=room)

        elif body.get("status") == 'INCOMING':  # 来电转分机请求
            vid = body.get("vid")
            ws['tran_id'] = body['vid']  # 将来访者id写入ws字典，供满意度调查按钮使用
            welcome(vid)

            # if setting_phone['pid']:  # 如果设置分机的优先级，使用优先分机
            #     auto(body['vid'], setting_phone['pid'])
            # else:
            #     pid = list(Funcs.p['IDLE'])  # 如果没有设置分机的优先机，就使用allFunc中的写死的默认分机
            #     # auto(body['vid'], random.choice(pid))             # 随机分配
            #     auto(body['vid'], '212')                            # 指定分机

        elif body.get("status") == 'change_status':  # 分机状态改变
            socketio.emit(event='phone_status', data=body)  # 广播给所有客户端，显示分机的状态

        elif body.get("status") == 'lose':  # 电话漏接情况，发送漏接短信
            pid = body['pid']               # 分机号
            client_phone = body['number']
            seat = Seat.query.filter_by(number=pid).first()
            user = seat.user
            user_phone = user.phone
            log('漏接短信信息', user_phone, client_phone, pid)
            status = send_message(user_phone, client_phone, pid)


# 接收OM的消息
@app.route('/ip_phone', methods=['GET', 'POST'])
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


# 运行服务器
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # qs = Query_Seats()
    # qs.query_all_seats()
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

    # app.run(**config) #开始运行服务器
