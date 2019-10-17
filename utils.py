import time
import subprocess
import requests


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)

# 根据seatId找到number账号,根据number账号找到room房间号
def getNumber(sid, Model, ws):
    log('执行getNumber函数')
    seat = Model.query.filter_by(number=sid).first()
    log('找到对应的座机')
    user = seat.user
    log('分机对应的账号', user.number)
    roomId = user.number  # 根据分机号找到账号
    room = ws.get(roomId)
    log(sid,'座机对应的的room号码', room)
    return room

# 根据座机号，找到对应的用户id
def get_uid(Model, pid):
    seat = Model.query.filter_by(number=pid).first()
    log('seat是否存在', seat)
    if seat:
        uid = seat.uid  # 找到seat对应的外键
    else:
        uid = 22
    return uid

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
    cmd = 'wget -P %s %s --http-user=user --http-password=user' % (om_config['audio_path'], Url)        # 从OM的Url上下载到计算机相应的地点om_config['audio_path']
    log('执行shell命令，60s之后下载录音...', cmd)
    time.sleep(60)  # 60s之后下载录音
    subprocess.call(cmd, shell=True)  # 将录音文件下载到服务器的指定文件夹中


# 用于分机优先级
pri_list = []

# 被引入到app.py文件中，找到分机
def get_phone(data, idle):
    get_pri_list(data)
    count = 0
    p = find_seat(data, idle, count)
    log('能得到的优先级最高的分机是', p)
    return p

# 递归，找到空闲且优先级较高的分机
def find_seat(data, idle, count):
    # log('在find_seat()中寻找pri_list', pri_list)
    v = findMin(pri_list)
    log('最小的数字', v)
    seat = get_key(data, v)
    log('得到的分机号码', seat)
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
        log('有优先级相同的座机，或者无相应的空闲分机...')


# 将前端的页面设置的分机加入优先级列表
def get_pri_list(data):
    for k, v in data.items():
        pri_list.append(v)
        log('依次加入分机优先级列表', pri_list)


# 通过value找到key,用此函数的前提是key和value必须唯一,否则返回空值。因此分机的优先级不可以重复
def get_key(dict, value):
    for k, v in dict.items():
        if v == value:
            return k


# 找到优先级的最小值
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
            # __dict__， 将类实例变成字典形式
            # [{id: 1, cid: 2, ...}, {id: 2, cid: 3, ...}, {id: 3, cid: 4, ...}, {id: 4, cid: 5, ...}]
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
    # 来电转分机
    # 'om_url': 'http://192.168.1.150/xml',  # OM20
    'om_url': 'https://fanyuan.tpddns.cn:1888/xml',  # OM50

    # 从OM服务器上下载录音文件地址
    # 'om_record_url': 'http://192.168.1.150/mcc/Recorder/',  # OM20
    'om_record_url': 'http://fanyuan.tpddns.cn:2888/mcc/Recorder/',  # OM50

    # 录音下载到本地服务器
    'audio_path': '/root/learngit/audio/',  # 阿里云服务器
    # 'audio_path': 'C:/Users/86177/Documents/GitHub/flaskWeb/audio/',  # 本地的录音文件

    # 图片文件所在地
    'img_path': '/root/learngit/images/',                             # 服务器
    # 'img_path': 'C:/Users/86177/Documents/GitHub/flaskWeb/audio/',      # 本地开发
}
