# import requests
# from flask_socketio import SocketIO, join_room, leave_room
# from utils import log, om_config, wget_down
# from allFuncs import Funcs
#
# from utils import get_phone, post_om
#
# socketio = SocketIO()
#
# ws = {           # ws的样例
#     '1763': '503d9587b1d34d39983cbe0400',
# }
#
#
# # 接收客户端的消息，
# @socketio.on('login')
# def send(data):
#     log('use webScoket receive sucessful', data)            # 数据以字典的形式传递过来的，{'data': '123'}
#     sid = request.sid           # io的客户端，用来标识唯一客户端。也是会话id
#     ws[data] = sid
#     log('查看ws字典', ws)
#     socketio.emit(event='test_room', data='connected')  # 私聊的功能
#
#
# # 电话会议
# @socketio.on('conference')
# def conference(data):
#     log('接收到%s的数据, 呼叫%s分机' % (data['phone'], data['phone']))
#     # 212是被呼叫的号码
#     body = '<Transfer attribute="Connect">\r\n<ext id="212"/>\r\n<ext id="%s"/>\r\n</Transfer>' % data['phone']
#     log(body)
#     post_om(body)
#
# # 让第三方进入电话会议
# @socketio.on('hold')
# def hold(data):
#     log('接收到hold', data)
#     # 发送212hold请求
#     h_body = '<Control attribute="Hold">\r\n<ext id="212"/>\r\n</Control>'
#     post_om(h_body)
#     # 让第三方会话接入
#     t_body = '<Transfer attribute="Connect">\r\n<ext id="212"/>\r\n<ext id="%s"/>\r\n</Transfer>' % data['hphone']
#     post_om(t_body)
#     # 执行conference命令
#     c_body = '<?xml version="1.0" encoding="utf-8" ?><Transfer attribute="Conference"><ext id="212"/></Transfer>'
#     post_om(c_body)
#
#
# # 触发满意度评价
# @socketio.on('satisfy')                     # 接收到消息转到语音播报
# def satisfy(data):
#     log('接收到点击按钮传递的信息', data)
#     # 发送语音评价
#     s_body = '<Transfer attribute="Connect"><visitor id="%s" /><menu id="1"/></Transfer>' % ws['tran_id']
#     log('转发到语音播报命令', s_body)
#     post_om(s_body)
#
#
# # 设置分机的优先级
# @socketio.on('priority')
# def setting_priority(data):
#     log('接收到设置优先级', data)
#     priori = {}
#     priori['priority'] = data
#     Funcs.p.update(priori)
#     log(Funcs.p)
#     get_phone(data, Funcs.p)