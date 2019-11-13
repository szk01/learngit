# 查询分机状态
from utils import log, om_config
import requests


class Query_Seats(object):
    # 查询分机状态
    def query_all_seats(self):
        payload = '<?xml version="1.0" encoding="utf-8" ?>\r\n' \
                  '<Control attribute="Query">\r\n' \
                  '<DeviceInfo/>\r\n' \
                  '</Control>'
        log('发送呼叫请求', payload)
        url = om_config['om_url']
        requests.request("POST", url, data=payload, verify=False)



