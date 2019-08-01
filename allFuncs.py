from excuteRequest import Process_request
import random
import xml.dom.minidom as xmldom
from excuteRequest import log



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
    #自动转分机功能
    def autoTransfer(self):
        event = self.getRoot()
        ext = event.getElementsByTagName('visitor')[0]
        visitor_id = ext.getAttribute("id")                 #访问者id

        #组成来电转分机请求
            #读取xml文件，并修改visitor的属性
        root = xmldom.parse('autoTransfer.xml')
        visitor = root.getElementsByTagName('visitor')[0]
        visitor.setAttribute("id", visitor_id)

            #随机取到idle的id，赋值给ext
        random_idle_id = random.choice(Funcs.p['IDLE'])     #随机取到IDLE的id
        ext = root.getElementsByTagName('ext')[0]
        ext.setAttribute("id", random_idle_id)
        print(root)
        return root

    #根据attribute调用函数
    def funcs(self):
        f = {
            'INVITE': self.autoTransfer,
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


