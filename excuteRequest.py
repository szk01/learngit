import xml.dom.minidom as xmldom
import time
import xml.etree.ElementTree as ET

def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


class Process_request(object):
        #类变量，将在所有的实例中共享

    def __init__(self, xml):         #xml是需要外部传入的变量
        self.xml = xml


    def getRoot(self):              #解析根节点
        dom = ET.fromstring(self.xml)
        # dom = xmldom.parse(self.xml)
        event = dom.documentElement
        log('getRoot():' ,event)
        return event

    #解析Event的attribute属性，根据这个属性分配不同的方法处理请求
    def getEvent_name(self):
        event = self.getRoot()
        event_name = event.getAttribute('attribute')
        log('getEvent_name():' ,event_name)
        return event_name

