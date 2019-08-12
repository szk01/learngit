from flask import (
    request,
    Blueprint,
)
import requests
from utils import log
from allFuncs import Funcs

main = Blueprint('OM', __name__)


# 给OM服务器发送一个POST请求
def reqestOM(body):
    url = 'https://zhidi.sfyf.cn:1888/xml'
    payload = body
    headers = {
        'content-type': 'text/xml',
    }
    requests.request("POST", url, data=payload, headers=headers, verify=False)


# 会使用到多线程，不同的进程处理不同的请求
@main.route('/ip_phone', methods=['GET'])
def ip_phone():
    log(request.method)
    xml = request.data  # 传过来的数据类型是byte类型
    xml = xml.decode('utf-8')
    # 开始处理各种请求
    log('OM向应用服务器发送的请求数据:', xml)
    # 将OM的请求数据清洗出来访者id
    funct = Funcs(xml)
    body = funct.funcs()
    log('发送给OM的请求：', body)
    # 接收到一个请求之后，发送一个请求
    # 只要body不为空，说明有请求需要发送
    if body is not None:
        reqestOM(body)
    return 'App Server sucess receive!'
