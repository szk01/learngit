import socket
import time
import random
import hashlib

def tcpsend(ip,port,xmlbw):


    #创建服务端的socket对象socketserver
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.SOL_TCP)
    #设定地址、端口号
    address = (ip,port)

    #建立链接
    client.connect(address)
    xmllen = len(xmlbw)
    sbw = ("POST /xml HTTP/1.1\r\nContent-Type:text/html\r\nHost:%s:%d\r\nContent-Length:%d\r\n\r\n%s") % (ip,port,xmllen,xmlbw)
    by = sbw.encode('utf8')
    #发送报文
    client.send(by)
    print("tcp发送成功")
    #接受响应信息
    data = client.recv(1024).decode('utf-8')
    print("接受响应成功")
    print(data)
    client.close()


def Http():
    bw = '<?xml version="1.0" encoding="utf-8" ?><Control attribute="Query"><DeviceInfo/></Control>'
    # bw = '<?xml version="1.0" encoding="utf-8" ?><Control attribute="Query"><exit id="215"/></Control>'

    ip = '180.175.33.122'
    port = 1888
    tcpsend(ip, port, bw)

Http()