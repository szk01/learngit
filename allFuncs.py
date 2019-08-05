from excuteRequest import Process_request
from excuteRequest import log
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import random


class Funcs(Process_request):
    #类变量，所有的实例共享这个变量
    p = {
            'BUSY': [],
            'IDLE': ['215'],
            'ONLINE': ['215'],
            'OFFLINE': [],
        }

    #加上请求头，组成完整请求
    def add_header(self, body):
        auth = '<Auth>\r\n' \
                     '<Timestamp>23</Timestamp>\r\n' \
                     '<nonce>23</nonce>\r\n' \
                     '<Signature>f42c335f75c1ea8577e98cbe3eeffbb3</Signature>\r\n' \
                     '</Auth>\r\n'
        body_type = '<?xml version="1.0" encoding="utf-8" ?>\r\n'
            #计算出body的长度
        body_len = len(auth) + len(body_type) + len(body)
        # body_len = len(body_type) + len(body)
        res_header = 'POST /xml HTTP/1.1\r\nContent-Type:text/xml\r\nContent-Length:{}\r\n\r\n'.format(body_len)
        res = res_header + body_type + auth + body
        return res

    #修改分机状态信息
    def phone_status(self):
        log('phone_status()执行')
        event = self.getRoot()
        event_name = self.getEvent_name()

        #拿到phone_id
        ext = event.getElementsByTagName('ext')[0]
        id = ext.getAttribute("id")
        if event_name == 'ONLINE':
            Funcs.p[event_name].append(id)          #加入在线组
            Funcs.p['IDLE'].append(id)              # 加入空闲组
            # p['OFFLINE'].remove(id)         #移出离线组

        # 忙事件报告
        if event_name == 'BUSY':
            log('phone_status:', event_name)
            Funcs.p[event_name].append(id)  # 加入忙组
            # Funcs.p['IDLE'].remove(id)  # 移出空闲组

        # 空闲事件报告
        if event_name == 'IDLE':
            Funcs.p[event_name].append(id)  # 加入空闲组
            Funcs.p['BUSY'].remove(id)  # 移出忙组

        # 离线事件报告
        if event_name == 'OFFLINE':
            Funcs.p[event_name].append(id)  # 加入离线组

            if id in Funcs.p['BUSY']:
                Funcs.p['BUSY'].remove(id)  # 移出忙组
            if id in Funcs.p['IDLE']:
                Funcs.p['IDLE'].remove(id)
            if id in Funcs.p['ONLINE']:
                Funcs.p['ONLINE'].remove(id)
        log(Funcs.p)

    #查询语音文件
    def Query_voice(self):
        body = '<Manage attribute="Query" >\r\n<voicefile/>\r\n</Manage>'
        response = self.add_header(body)
        log('查询语音文件命令执行')
        return response

    #对INCOMING事件进行处理,转到分机处理
    def autoTransfer(self):
        event = self.getRoot()
        ext = event.find('visitor')
        visitor_id = ext.attrib['id']                 #访问者id
        #组成来电转分机请求
            #读取xml文件，并修改visitor的属性
        autoText = '<Transfer attribute="Connect">\r\n<visitor id="14"/>\r\n<ext id="215"/>\r\n</Transfer>'
            #解析xml字符串
        root = ET.fromstring(autoText)
        visitor = root.find('visitor')
        visitor.set('id', visitor_id)
            #随机取到idle的id，赋值给ext
        random_idle_id = random.choice(Funcs.p['IDLE'])      #随机取到IDLE的id
        ext = root.find('ext')
        ext.set('id', random_idle_id)
        log('autoTransfer():', root)                         #应该是Transfer
        log('来访者id:', root.find('visitor').attrib['id'])
        log('转接分机id:', root.find('ext').attrib['id'])
        res_body = tostring(root, encoding='utf-8')          #res_body是bytes类型的数据
        res_body = res_body.decode('utf-8')                  #现在转成字符串utf-8类型

        response = self.add_header(res_body)
        # res = Funcs.res_header + res_body
        # res.encode('utf-8')
        return response

    #根据attribute调用函数
    def funcs(self):
        #可能少了一个判断root的tag
        f = {
            'INCOMING':self.autoTransfer,
            'INVITE': '',
            'BUSY': self.phone_status,
            'IDLE': self.phone_status,
            'ONLINE': self.phone_status,
            'OFFLINE': self.phone_status,
        }
        eventName = self.getEvent_name()
        # log('func:', eventName)
        result = f.get(eventName, '未找到相应的函数处理')      #返回的是相应的函数地址
        if type(result) != str:
            res = result()                            #找到则调用这个函数
            return res
        else:
            log(result)                         #没有找到就打印,没有找到这个函数

        # log('result:' ,result)



# dom = xmldom.parse('busy.xml')
# funct = Funcs(dom)
# funct.funcs()


