import time
import subprocess
import requests


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


# 给OM服务器发送一个POST请求
def post_om(body):
    body_type = '<?xml version="1.0" encoding="utf-8" ?>\r\n'
    payload = body_type + body
    log('给om发送请求', payload)
    url = om_config['om_url']
    requests.request("POST", url, data=payload, verify=False)


# 发送来电转分机请求
def auto(vid, pid):
    payload = '<?xml version="1.0" encoding="utf-8" ?>\r\n<Transfer attribute="Connect">\r\n<visitor id="%s"/>\r\n<ext ' \
              'id="%s"/>\r\n</Transfer>' % (vid, pid)
    log('发送呼叫请求', payload)
    url = om_config['om_url']
    requests.request("POST", url, data=payload, verify=False)


# 用于app文件，下载录音文件
def wget_down(Url):
    cmd = 'wget -P %s %s --http-user=user --http-password=user' % (om_config['path'], Url)
    log('执行shell命令，60s之后下载录音...', cmd)
    time.sleep(60)  # 60s之后下载录音
    subprocess.call(cmd, shell=True)  # 将录音文件下载到服务器的指定文件夹中


# 用于分机优先级
pri_list = []


def get_phone(data, idle):
    get_pri_list(data)
    count = 0
    find_seat(data, idle, count)


def find_seat(data, idle, count):
    # log('在find_seat()中寻找pri_list', pri_list)
    v = findMin(pri_list)
    log('最小的数字', v)
    seat = get_key(data, v)
    log('得到的分机号码', seat, type(seat))
    if seat:  # 如果找到优先级最高的seat
        # log('空闲分组中存在的分机', idle['IDLE'])
        if seat in idle['IDLE']:  # 并且座机空闲
            log('优先级最高且是空闲座机,返回此分机', seat)
            return seat  # 递归出口
        else:  # 座机忙碌，那么找到第二优先级的空闲座机
            count += 1
            pri_list.remove(v)
            log('第%s次迭代' % count)
            find_seat(data, idle, count)  # 递归
    else:
        log('有优先级相同的座机，请在页面上重新选择')


# 得到优先级列表
def get_pri_list(data):
    for k, v in data.items():
        pri_list.append(v)
        log(pri_list)


# 通过value找到key,用此函数的前提是key和value必须唯一,否则返回空值
def get_key(dict, value):
    for k, v in dict.items():
        if v == value:
            return k


# 找到最小值
def findMin(list):
    if len(list):
        min = list[0]
        for i in list:
            if i < min:
                min = i
        return min
    else:
        log('设置出错，请联系管理员...')


# 将model对象序列化成dict对象
def serialize(result):
    from collections import Iterable
    # 转换完成后，删除  '_sa_instance_state' 特殊属性
    try:
        if isinstance(result, Iterable):
            tmp = [dict(zip(res.__dict__.keys(), res.__dict__.values())) for res in result]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp
    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')


# 配置文件
om_config = {
    # 'om_url': 'http://192.168.1.150/xml',  # 给om发送来电转分机，post请求的地址
    'om_url': 'https://fanyuan.tpddns.cn:1888/xml',  # 上海那边的om50,发送来电转分机请求
    'app_record_url': 'http://106.15.44.224/audio/',  # 浏览器获取服务器录音文件的地址
    'om_record_url': 'http://192.168.1.150/mcc/Recorder/',  # 深圳om20存储录音文件的地址
    # 'om_record_url': 'http://101.81.125.16:2888/mcc/Recorder/',  # 上海om50存储录音文件的地址
    'path': '/root/learngit/audio',  # 录音下载到阿里云服务器的路径
    # 'path': 'C:/Users/86177/Documents/GitHub/flaskWeb/audio'  # 录音下载到本地电脑上的路径，也是audio的播放路径
}
