'''
ivr功能导航
1, 对按键事件DTMF进行处理
2, 异常处理，输入超时
            输入错误，    两者可以使用 临时替换语音文件 功能
3, DTMF直接按分机号码

3, 判断由谁来接电话
4, 可以被allFuncs继承

财务1， 客服2， 操作3，
按键为1：
    找出角色为财务的用户，
    计量他们的phone_count数量，找到最小值
    转接
'''
from utils import om_config, log
import requests
from models.user import User
from models.seat import Seat


class Ivr(object):
    # 给om发送请求
    @staticmethod
    def post_om(body):
        body_type = '<?xml version="1.0" encoding="utf-8" ?>\r\n'
        payload = body_type + body
        log('给om发送请求', payload)
        url = om_config['om_url']
        requests.request("POST", url, data=payload, verify=False)

    # 根据value值从dict找到最小那组
    @staticmethod
    def find_min(dict):
        r = min(dict.items(), key=lambda x: x[1])
        return r[0]

    # 根据id找到对应的seat
    @staticmethod
    def get_seat(id):
        seat = Seat.query.filter_by(uid=id).first()
        return seat.name

    # 将model对象的id和phone_count组成字典
    @staticmethod
    def dict_composed_filed(ms):
        from collections import Iterable

        if isinstance(ms, Iterable):
            r = {}
            for m in ms:
                r[m.id] = m.phone_count
            return r
        elif ms is None:
            log('没有找到这个角色')

    # 根据mid找到不同的Model
    @staticmethod
    def get_models(mid):
        if mid == '1':
            return User.query.filter_by(rid=5).all()
        elif mid == '2':
            return User.query.filter_by(rid=1).all()
        elif mid == '3':
            return User.query.filter_by(rid=3).all()

    # 根据mid找到对应的值
    @staticmethod
    def kinds(dtmf):
        seeds = '123'
        if len(dtmf) == 1 and dtmf in seeds:                    # 按正常的按键
            return 'exist_dtmf'
        elif len(dtmf) == 3 and dtmf[0] == '2':                 # 直接按分机号
            return 'exist_seat'
        else:                                                   # 按键异常
            return 'error'

    # 根据按键找到最小值
    def excute_dtmf(self, mid):
        ms = Ivr.get_models(mid)
        d = Ivr.dict_composed_filed(ms)
        uid = Ivr.find_min(d)
        seat = Ivr.get_seat(uid)  # 找到对应的座机，发送请求
        log('ivr seat', seat)
        return seat

    # 按键为分机号,来电转分机
    def mid_is_seat(self, vid, pid):
        payload = '<?xml version="1.0" encoding="utf-8" ?>\r\n<Transfer attribute="Connect">\r\n<visitor ' \
                  'id="%s"/>\r\n<ext ' \
                  'id="%s"/>\r\n</Transfer>' % (vid, pid)
        log('发送呼叫请求', payload)
        url = om_config['om_url']
        requests.request("POST", url, data=payload, verify=False)

    # 按键异常，播放提示音，临时替换语音文件
    def dtmf_error(self, vid):
        error = '<Transfer attribute="Connect"><visitor id="%s" />user_welcome150646+userivr1<menu id="6"/></Transfer>' % vid
