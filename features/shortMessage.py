#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json


def send_message(user_number, number, seat):
    client = AcsClient('LTAI4FhevV5YD3MeHbkKg3BJ', 'RahvWU7RUzkZHUZyqZ00i1u25IJh8q', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', user_number)
    # request.add_query_param('PhoneNumbers', "17730523795")
    request.add_query_param('SignName', "上海泛远")            # 签名
    request.add_query_param('TemplateCode', "SMS_175541249")
    # request.add_query_param('TemplateParam', "{\"customer\":\"Robert\"}")
    request.add_query_param('TemplateParam', "{\"number\":\"%s\",\"seat\":\"%s\"}"% (number, seat))           # 需要拼接字符串

    response = client.do_action(request)
    # print('返回的response', type(response))
    r = str(response, encoding='utf-8')
    status = json.loads(r).get('Message')
    return status
    # python2:  print(response)


# if __name__ == '__main__':
#     # 会返回状态码，
#     s = send_message()
