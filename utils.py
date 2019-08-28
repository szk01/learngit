import time


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


# 配置文件
om_config = {
    'om_url': 'https://192.168.101.15/xml',                         # 给om发送来电转分机，post请求的地址
    'app_record_url': 'http://106.15.44.224/audio/',                        # 浏览器获取服务器录音文件的地址
    'om_record_url': 'http://192.168.101.15/mcc/Recorder/',         # om存储录音文件的地址
    'linux_path': '/root/learngit/audio',                                    # 录音下载到服务器本地的路径
}