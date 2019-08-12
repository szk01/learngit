import xml.etree.ElementTree as ET
import time


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


class Process_request(object):
    # 类变量，将在所有的实例中共享

    def __init__(self, xml):  # xml是需要外部传入的变量
        self.xml = xml

    def getRoot(self):  # 解析根节点
        # dom = xmldom.parse(self.xml)
        root = ET.fromstring(self.xml)
        log('getRoot():', root.tag)
        if root.tag == 'Event':
            return root
        elif root.tag == 'Cdr':
            log('暂不处理话单请求')

    # 解析Event事件报告的attribute属性，根据这个属性分配不同的方法处理请求
    def getEvent_name(self):
        root = self.getRoot()
        try:
            attriName = root.attrib['attribute']
            log('getEvent_name():', attriName)
            return attriName
        except:
            log('root为空，OM请求不是事件报告，暂时并不处理')
