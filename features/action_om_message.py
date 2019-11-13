# 根据消息处理请求,替代app.py文件中extcute_body()函数
# 来电转分机
from utils import om_config, log
from Socket.scoket import ws, socketio                # ws肯定是在路由和websocket之间传输
import requests
from models.seat import Seat


class ActionMessage(object):

    def __init__(self, dict_message):       # dict_message是allFuncs中的类传过来的字典
        self.dm = dict_message

    # 根据seatId找到number账号,根据number账号找到room房间号
    @staticmethod
    def getNumber(sid, Model, ws):
        log('执行getNumber函数')
        seat = Model.query.filter_by(number=sid).first()
        user = seat.user
        if user:
            log('分机对应的账号', user.number)
            roomId = user.number  # 根据分机号找到账号
            room = ws.get(roomId)
            log(sid, '座机对应的的room号码', room)
            return room
        else:
            log('找不到相应的座机号')

    # status: Transfer, 来电转分机动作   pid需要主逻辑传入
    def transfer_to_seat(self, pid):
        vid = self.dm.get("vid")
        payload = '<?xml version="1.0" encoding="utf-8" ?>\r\n<Transfer attribute="Connect">\r\n<visitor ' \
                  'id="%s"/>\r\n<ext ' \
                  'id="%s"/>\r\n</Transfer>' % (vid, pid)
        log('发送来电转分机请求', payload)
        url = om_config['om_url']
        requests.request("POST", url, data=payload, verify=False)

    # 处理各种不同的body
    def extcute_body(self, body):
        if isinstance(body, dict):

            if body.get("status") == "RING":  # 有电话接入call-in，客户端显示页面
                log(body["number"])
                log('有电话接入，显示弹窗')
                ws['tran_id'] = body['vid']  # 将来访者id写入ws字典，供满意度调查按钮使用
                seatId = body['pid']  # seatId是分机号
                room = ActionMessage.getNumber(seatId, Seat, ws)
                socketio.emit(event='ring', data=body, room=room)

            elif isinstance(body.get('ws'), dict):
                log('通话结束传过来的body', body)
                if body['ws']['status'] == 'Cdr':
                    # 通话结束，发送Cdr话单，包含录音文件的路径
                    log('通话结束，停止计时')
                    seatId = body['ws']['pid']
                    room = ActionMessage.getNumber(seatId, Seat, ws)
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

            elif body.get("status") == 'Transfer':  # 来电转分机请求
                log('发送来电转分机请求')
                ws['tran_id'] = body['vid']  # 将来访者id写入ws字典，供满意度调查按钮使用
                if setting_phone['pid']:  # 如果设置分机的优先级，使用优先分机
                    auto(body['vid'], setting_phone['pid'])
                else:
                    pid = list(Funcs.p['IDLE'])  # 如果没有设置分机的优先机，就使用allFunc中的写死的默认分机
                    # auto(body['vid'], random.choice(pid))             # 随机分配
                    auto(body['vid'], '221')  # 指定分机

            elif body.get("status") == 'change_status':  # 分机状态改变
                socketio.emit(event='phone_status', data=body)  # 广播给所有客户端，显示分机的状态
        elif body == "lose":
            log("发送漏接短信")
            status = send_message("17730523795")
            log('得到发送的status', status)


