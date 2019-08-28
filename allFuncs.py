from excuteRequest import Process_request
from excuteRequest import log
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import random
import time
import subprocess  # 用来调用命令行shell
from utils import config


class Funcs(Process_request):
    # 类变量，所有的实例共享这个变量
    p = {
        'BUSY': set(),
        'IDLE': {'2'},
        'ONLINE': {'2'},
        'OFFLINE': set(),
    }

    # 加上请求头，组成完整请求
    @staticmethod
    def add_header(body):
        body_type = '<?xml version="1.0" encoding="utf-8" ?>\r\n'
        req = body_type + body
        return req

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

        # 忙事件报告
        if event_name == 'BUSY':
            log('phone_status:', event_name)
            Funcs.p[event_name].add(id)  # 加入忙组
            Funcs.p['IDLE'].discard(id)  # 移出空闲组

        # 空闲事件报告
        if event_name == 'IDLE':
            Funcs.p[event_name].add(id)  # 加入空闲组
            Funcs.p['BUSY'].remove(id)  # 移出忙组

        # 离线事件报告
        if event_name == 'OFFLINE':
            Funcs.p[event_name].add(id)  # 加入离线组
            if id in Funcs.p['BUSY']:
                Funcs.p['BUSY'].remove(id)  # 移出忙组
            if id in Funcs.p['IDLE']:
                Funcs.p['IDLE'].remove(id)  # 移出空闲组
            if id in Funcs.p['ONLINE']:
                Funcs.p['ONLINE'].remove(id)  # 移出在线组
        log(Funcs.p)

    # 查询语音文件
    def Query_voice(self):
        body = '<Manage attribute="Query" >\r\n<voicefile/>\r\n</Manage>'
        response = self.add_header(body)
        log('查询语音文件命令执行')
        return response

    # 对INCOMING事件进行处理,转到分机处理返回请求数据
    def autoTransfer(self):
        event = self.getRoot()
        ext = event.find('visitor')
        visitor_id = ext.attrib['id']  # 访问者id
        # 组成来电转分机请求
        # 读取xml文件，并修改visitor的属性
        autoText = '<Transfer attribute="Connect">\r\n<visitor id="14"/>\r\n<ext id="215"/>\r\n</Transfer>'
        # 解析xml字符串
        root = ET.fromstring(autoText)
        visitor = root.find('visitor')
        visitor.set('id', visitor_id)
        # 随机取到idle的id，赋值给ext
        random_idle_id = random.choice(list(Funcs.p['IDLE']))  # 随机取到IDLE的id
        ext = root.find('ext')
        ext.set('id', random_idle_id)
        log('autoTransfer():', root)  # 应该是Transfer
        log('来访者id:', root.find('visitor').attrib['id'])
        log('转接分机id:', root.find('ext').attrib['id'])
        req_body = tostring(root, encoding='utf-8')  # res_body是bytes类型的数据
        req_body = req_body.decode('utf-8')  # 现在转成字符串utf-8类型

        data = Funcs.add_header(req_body)
        return data

    # 对（来电转分机触发）振铃事件RING 进行处理，发送客户端的号码
    def alterWin(self):
        event = self.getRoot()
        mes = event.find('visitor')
        number = mes.attrib['from']  # 来电id
        log('来电号码', number)
        res = {"number": number, "status": "RING"}
        return res

    # 对ANWSER事件处理，分机应答后，发送状态
    def status_change(self):
        return 'ANWSER'

    # 通话结束后，拿到录音的相对路径，下载录音到服务器上，返回来电号码
    def recording(self):
        event = self.getRoot()
        number = event.find('CPN').text
        cdr_type = event.find('Type').text
        if cdr_type == 'LO':  # 只处理类型为LO的话单
            log('recording()', number)
            # recording = event.find('Recording')
            # record_name = recording.text
            # play_path = config['app_server_url'] + record_name
            # log('输出相对路径', path)
            # competeUrl = config['om_record_url'] + record_name                     # 下载地址
             # log('完整路径：', competeUrl)
            #
            # cmd = '/usr/bin/wget -P %s %s' % (config['linux_path'], competeUrl)
            # log('执行shell命令，5s之后下载录音...', cmd)
            # time.sleep(10)  # 5s之后下载录音
            # subprocess.call(cmd, shell=True)             # 将录音文件下载到服务器的指定文件夹中

            play_path = ''
            competeUrl = ''
            res = {"play": play_path, "downPath": competeUrl, "status": "Cdr", "number": number}
            return res

    # 根据attribute调用请求函数
    def funcs(self):
        # 可能少了一个判断root的tag
        f = {
            'Cdr': self.recording,  # 话单请求，返回两个录音文件路径
            # 'BYE': self.call_end,   # 来电和分机通话结束，返回来电号码
            'ANSWER': self.status_change,  # 来电转分机分机应答，通话建立
            'RING': self.alterWin,  # 来电 弹窗显示号码，正在呼叫
            'INCOMING': self.autoTransfer,
            'BUSY': self.phone_status,
            'IDLE': self.phone_status,
            'ONLINE': self.phone_status,
            'OFFLINE': self.phone_status,
        }
        eventName = self.getEvent_name()
        # log('func:', eventName)
        result = f.get(eventName, '未找到相应的函数处理')  # 返回的是相应的函数地址
        try:
            res = result()  # 调用这个函数
            return res
        except Exception as e:
            log(e)  # 没有找到就打印,没有找到这个函数

        # log('result:' ,result)

# dom = xmldom.parse('busy.xml')
# funct = Funcs(dom)
# funct.funcs()
