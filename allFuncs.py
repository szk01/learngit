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


    #对INVITE事件进行处理,接受invite请求
    def accept(self):
    #获取来电id
        event = self.getRoot()
        ext = event.find('visitor')
        visitor_id = ext.attrib['id']
    #组成accept请求
        ap = '<?xml version="1.0" encoding="utf-8" ?><Notify attribute="Accept"><visitor id="1"/></Notify>'
        root = ET.fromstring(ap)
        visitor = root.find('visitor')
        visitor.set('id', visitor_id)
        return root.tostring()


    #对INCOMING事件进行处理,转到分机处理
    def autoTransfer(self):
        event = self.getRoot()
        ext = event.find('visitor')
        visitor_id = ext.attrib['id']                 #访问者id
        #组成来电转分机请求
            #读取xml文件，并修改visitor的属性
        autoText = '<?xml version="1.0" encoding="utf-8" ?><Transfer attribute="Connect"><visitor id="14"/><ext id="215"/><voicefile>silence+silence+connect</voicefile></Transfer>'
        root = ET.fromstring(autoText)
        visitor = root.find('visitor')
        visitor.set('id', visitor_id)
            #随机取到idle的id，赋值给ext
        random_idle_id = random.choice(Funcs.p['IDLE'])     #随机取到IDLE的id
        ext = root.find('ext')
        ext.set('id', random_idle_id)
        log('autoTransfer():', root)                         #应该是Transfer
        log('来访者id:', root.find('visitor').attrib['id'])
        log('转接分机id:', root.find('ext').attrib['id'])
        return root.tostring()

    #根据attribute调用函数
    def funcs(self):
        #可能少了一个判断root的tag
        f = {
            'INCOMING':self.autoTransfer,
            'INVITE': self.accept,
            'BUSY': self.phone_status,
            'IDLE': self.phone_status,
            'ONLINE': self.phone_status,
            'OFFLINE': self.phone_status,
        }
        eventName = self.getEvent_name()
        log('func:', eventName)
        result = f.get(eventName, 'none_func')      #返回的是相应的函数地址
        if type(result) != str:
            result()
        else:
            log(result)
        # log('result:' ,result)



# dom = xmldom.parse('busy.xml')
# funct = Funcs(dom)
# funct.funcs()


