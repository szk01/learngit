from flask import session, request
from flask_socketio import SocketIO
from utils import om_config, get_phone, log
import requests
from allFuncs import Funcs

socketio = SocketIO()

# 绑定分机号和io客户端标识,sid
# 塞入来电的vid, 以供满意度调查按钮使用
ws = {}

# 存储来电转分机的分机号
setting_phone = {
    'pid': None,
}


# 给OM发送请求
def post_om(body):
    body_type = '<?xml version="1.0" encoding="utf-8" ?>\r\n'
    payload = body_type + body
    log('发送呼叫请求', payload)
    url = om_config['om_url']
    requests.request("POST", url, data=payload, verify=False)


@socketio.on('login')
def send(data):
    log('use webScoket receive sucessful', data)
    log('接收到登录信息中的工号', data)
    data = session.get('number')
    sid = request.sid  # io的客户端，用来标识唯一客户端。也是会话id
    ws[data] = sid
    log('查看ws字典', ws)


# 电话会议
@socketio.on('conference')
def conference(data):
    log('接收到%s的数据, 呼叫%s分机' % (data['phone'], data['phone']))
    # 213呼叫号码
    body = '<Transfer attribute="Connect">\r\n<ext id="213"/>\r\n<ext id="%s"/>\r\n</Transfer>' % data[
        'phone']  # 213是写死的
    log(body)
    post_om(body)


# 触发满意度评价
@socketio.on('satisfy')
def satisfy(data):
    log('点击满意度调查按钮', data)
    # 发送语音评价
    s_body = '<Transfer attribute="Connect"><visitor id="%s" /><menu id="1"/></Transfer>' % ws['tran_id']
    log('转发到语音播报命令', s_body)
    post_om(s_body)


# 设置分机的优先级
@socketio.on('priority')
def setting_priority(data):
    log('接收到设置优先级', data)
    priori = {}
    priori['priority'] = data
    Funcs.p.update(priori)  # 前端发送过来的优先级设置，更新到allFuncs中的分机设置
    log('前台页面想要设置的分机优先级：', Funcs.p)
    set_phone = get_phone(data, Funcs.p)  # 拿到优先级最高的分机
    log('能得到的分机是', set_phone)
    if set_phone:
        setting_phone['pid'] = set_phone
    else:
        log('分机优先级设置失败')

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





