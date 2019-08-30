import time


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


# 配置文件
om_config = {
    'om_url': 'http://113.87.186.205:20080/xml',                         # 给om发送来电转分机，post请求的地址
    'app_record_url': 'http://106.15.44.224/audio/',              # 浏览器获取服务器录音文件的地址
    'om_record_url': 'http://192.168.1.150/mcc/Recorder/',        # om存储录音文件的地址
    'linux_path': '/root/learngit/audio',                         # 录音下载到阿里云服务器的路径
    'win_path': 'C:/Users/86177/Documents/GitHub/flaskWeb/audio'  # 录音下载到本地电脑上的路径
}