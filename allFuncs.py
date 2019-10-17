from excuteRequest import Process_request
from excuteRequest import log
import random
import time, asyncio
import subprocess  # 用来调用命令行shell
from utils import om_config, wget_down, post_om
from models.record import Call_record, Voice_record, db
from utils import get_phone


class Funcs(Process_request):
    # 类变量，所有的实例共享这个变量
    p = {
        'BUSY': set(),
        'IDLE': set(),                    # 当前端页面设置了分机的优先级，使用此分机进行测试
        'ONLINE': set(),
        'OFFLINE': set(),
        'pid': '213',                         # 写死的默认分机，前端没有设置分机优先的时候，使用此分机
        'priority': {                      # 这是默认优先级，数字越小，优先级越高。这些数据并没有用，只是前台设置后的demo示例
            '212': 1,
            '213': 2,
            '214': 3,
        }
    }
    # 每一通电话的三个时间节点
    time = {
        'start_time': None,  # 电话的打入时间
        'on_time': None,  # 电话的接通时间
        'end_time': None,  # 电话的结束时间
    }

    # 加上请求头，组成完整请求
    # 静态方法，只限于类使用，实例是不能使用的
    @staticmethod
    def add_header(body):
        body_type = '<?xml version="1.0" encoding="utf-8" ?>\r\n'
        req = body_type + body
        return req

    # 添加通话记录到mysql数据库
    @staticmethod
    def sql_addCallRecord(cr, uid):
        if Funcs.time['end_time']:

            log('静态方法，添加通话记录')
            log('插入到数据库中的字典', cr)
            call_record = Call_record(phone=cr['phone'], name=cr['name'], type=cr['type'],
                                      start_time=Funcs.time['start_time'], on_time=Funcs.time['on_time'],
                                      end_time=Funcs.time['end_time'], uid=uid,
                                      )
            log(Funcs.time)
            db.session.add(call_record)
            log('在数据库加入一条通话记录...')
            db.session.commit()

    # 添加录音记录到mysql数据库
    @staticmethod
    def sql_addVoiceRecord(vr, uid):
        voice_record = Voice_record(name=vr['name'], url=vr['url'], play_count=vr['play_count'],
                                    down_count=vr['down_count'], uid=uid
                                    )
        db.session.add(voice_record)
        log('在数据库加入一条录音记录...')
        db.session.commit()

    @staticmethod  # 获取时间戳
    def get_time():
        t = time.time()
        return int(t)

    # 处理Cdr话单消息,得到通话录音名
    @staticmethod
    def get_record_name(event):
        recording = event.find('Recording')
        if recording is not None:
            record_name = recording.text                # 语音文件名
            return record_name


    # 修改分机状态信息
    def phone_status(self):
        log('phone_status()执行')
        event = self.getRoot()
        event_name = self.getEvent_name()

        # 拿到phone_id
        # 分机上线
        id = event.find('ext').attrib['id']
        if event_name == 'ONLINE':
            Funcs.p[event_name].add(id)  # 加入在线组
            Funcs.p['IDLE'].add(id)  # 加入空闲组
            Funcs.p['OFFLINE'].discard(id)  # 移出离线组
            p = {'id': id, 'status': 'change_status', 'phone_status': '空闲'}
            return p                                # 发送给前端页面，显示分机状态

        # 忙事件报告
        if event_name == 'BUSY':
            log('phone_status:', event_name)
            Funcs.p[event_name].add(id)  # 加入忙组
            Funcs.p['IDLE'].discard(id)  # 移出空闲组
            p = {'id': id, 'status': 'change_status', 'phone_status': '忙线'}
            return p                                # 发送给前端页面，显示分机状态

        # 空闲事件报告
        if event_name == 'IDLE':
            Funcs.p[event_name].add(id)  # 加入空闲组
            Funcs.p['BUSY'].remove(id)  # 移出忙组
            p = {'id': id, 'status': 'change_status', 'phone_status': '空闲'}
            return p                                # 发送给前端页面，显示分机状态

        # 离线事件报告
        if event_name == 'OFFLINE':
            Funcs.p[event_name].add(id)  # 加入离线组
            if id in Funcs.p['BUSY']:
                Funcs.p['BUSY'].remove(id)  # 移出忙组
            if id in Funcs.p['IDLE']:
                Funcs.p['IDLE'].remove(id)  # 移出空闲组
            if id in Funcs.p['ONLINE']:
                Funcs.p['ONLINE'].remove(id)  # 移出在线组
            p = {'id': id, 'status': 'change_status', 'phone_status': '离线'}
            return p                                # 发送给前端页面，显示分机状态

    # 查询语音文件
    def Query_voice(self):
        body = '<Manage attribute="Query" >\r\n<voicefile/>\r\n</Manage>'
        response = Funcs.add_header(body)
        log('查询语音文件命令执行')
        return response

    # 对INCOMING事件进行处理,转到分机处理返回请求数据
    def autoTransfer(self):
        event = self.getRoot()
        ext = event.find('visitor')
        vid = ext.attrib['id']  # 访问者id
        t = {
            'vid': vid,
            'status': 'Transfer',
        }
        return t

    # 对（来电转分机触发）振铃事件RING 进行处理，发送客户端的号码。显示弹窗
    def alterWin(self):
        start_time = Funcs.get_time()  # 客户打入时间
        Funcs.time['start_time'] = start_time  # 更新打入时间
        log('填写start_time时间段', Funcs.time)

        event = self.getRoot()
        mes = event.find('visitor')
        number = mes.attrib['from']  # 来电id
        e = event.find('ext')
        pid = e.attrib['id']  # 转接的分机号码
        log('来电号码', number)
        log('被呼叫的分机号码:', pid)
        res = {"number": number, "pid": pid, "status": "RING"}
        log('发送给ws', res)
        return res

    # 对ANWSER事件处理，分机应答后，发送状态，计时器开始计数
    def status_change(self):
        on_time = Funcs.get_time()  # 电话接通时间
        Funcs.time['on_time'] = on_time  # 更新接通时间
        log('填写start_time和on_time', Funcs.time)

        log('执行函数status_change()')
        event = self.getRoot()
        mes = event.find('ext')
        pid = mes.attrib['id']  # 被呼叫的分机号码
        log('被呼叫的分机号码: ', pid)
        res = {"pid": pid, "status": "ANWSER"}
        return res


    # 通话结束后，拿到录音的相对路径，下载录音到服务器上，返回来电号码
    def recording(self):
        event = self.getRoot()
        # 拿到通话记录
        record_name = Funcs.get_record_name(event)
        if record_name is not None:
            Funcs.time['end_time'] = Funcs.get_time()  # 填入结束时间
            number = event.find('CPN').text  # 来电手机号
            pid = event.find('CDPN').text  # 分机号
            play_path = 'audio/' + record_name
            omUrl = om_config['om_record_url'] + record_name  # 存储在om上的录音文件地址，给wget下载

            log('完整路径：', omUrl)

            r = {}
            cr = {  # 通话记录，传到app.py文件中，加上文件
                "phone": number,
                "name": "未知",
                "type": 1,

            }

            vr = {  # 录音记录，
                "name": record_name,
                "url": play_path,
                "play_count": 0,
                "down_count": 0,

            }

            ws = {  # 发送给ws客户端的消息，传到app.py文件中，传给网页客户端
                "status": "Cdr",
                "number": number,
                "downPath": omUrl,
                "play": play_path,
                "pid": pid,  # 分机号
            }
            r['cr'] = cr
            r['vr'] = vr
            r['ws'] = ws

            return r

    #OM重启会配置满意度调查音乐
    def assign(self):
        # 配置menu1,满意度评价
        # 上海OM50的录音文件   user_welcome160431      user_welcome160927     user_welcome160523
        # 深圳OM20的录音文件   user_welcome153149      user_welcome153531     user_offhour153419
        menu1 = '<Control attribute="Assign"><menu id="1"><voicefile>user_welcome160431</voicefile><repeat>3</repeat' \
                '><infolength>1</infolength><exit>#</exit></menu></Control> '
        post_om(menu1)
        # 配置menu2，超时
        menu2 = '<Control attribute="Assign"><menu id="2"><voicefile>user_welcome160927</voicefile><repeat>1</repeat' \
                '><infolength>1</infolength><exit>#</exit></menu></Control> '
        post_om(menu2)
        # 配置menu3，感谢来电
        menu3 = '<Control attribute="Assign"><menu id="3"><voicefile>user_welcome160523</voicefile><repeat>1</repeat' \
                '><exit>#</exit></menu></Control> '
        post_om(menu3)

    # 处理DTMF的事件，接收到客户的按键信息。转到语音文件三
    def satisfy_audio(self):
        event = self.getRoot()
        visitor = event.find('visitor')
        menu = visitor.find('menu')
        # log('DTMF中的visitor', visitor)
        # log('DTMF中的menu', menu)
        vid = visitor.attrib['id']
        mid = menu.attrib['id']
        if mid == "1":  # 接收到客户的按键信息，按键为1
            m = '<Transfer attribute="Connect"><visitor id="%s" /><menu id="3"/></Transfer>' % vid
            post_om(m)  # 转接到语音菜单3

    # 菜单2或3播报完，收到endofAnn事件，执行挂断电话命令
    def clear(self):
        event = self.getRoot()
        vid = event.find('visitor').attrib['id']
        mid = event.find('menu').attrib['id']
        if mid == '3':  # 语音菜单三(感谢来电)播报完，挂断消息
            c_body = '<Control attribute="Clear"><visitor id="%s"/></Control>' % vid
            post_om(c_body)
        if mid == "1":
            m = '<Transfer attribute="Connect"><visitor id="%s" /><menu id="2"/></Transfer>' % vid  # 重复三次（做出评价）完。播报菜单2，超时播报
            post_om(m)
        if mid == "2":
            c_body = '<Control attribute="Clear"><visitor id="%s"/></Control>' % vid  # 超时挂断电话
            post_om(c_body)

    # 根据attribute调用请求函数
    def funcs(self):
        # 可能少了一个判断root的tag
        f = {
            'Cdr': self.recording,  # 话单请求，返回两个录音文件路径            2.6.2/LO
            # 'BYE': self.call_end,        # 来电和分机通话结束，返回来电号码
            'ANSWER': self.status_change,  # 来电转分机分机应答，通话建立              2.5.3
            'RING': self.alterWin,  # 来电 弹窗显示号码，正在呼叫               2.5.3
            'INCOMING': self.autoTransfer,
            'BUSY': self.phone_status,
            'IDLE': self.phone_status,
            'ONLINE': self.phone_status,
            'OFFLINE': self.phone_status,
            'BOOTUP': self.assign,  # 每次重启设置三个语音menu
            'DTMF': self.satisfy_audio,  # 收到DTMF事件，(客户按键)，转到语音三（感谢来电）
            'EndOfAnn': self.clear  # endofAnn事件,超时或者播放menu3语音文件完会收到，挂断事件
        }
        eventName = self.getEvent_name()
        # log('func:', eventName)
        result = f.get(eventName, '未找到相应的函数处理')  # 返回的是相应的函数地址
        try:
            res = result()  # 调用这个函数
            return res
        except Exception as e:
            log(e)  # 没有找到就打印,没有找到这个函数


