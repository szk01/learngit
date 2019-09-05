import time
import subprocess


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


# 用于app文件，下载录音文件
def wget_down(Url):
    cmd = 'wget -P %s %s --http-user=user --http-password=user' % (om_config['win_path'], Url)
    log('执行shell命令，10s之后下载录音...', cmd)
    time.sleep(60)  # 60s之后下载录音
    subprocess.call(cmd, shell=True)  # 将录音文件下载到服务器的指定文件夹中


# 配置文件
om_config = {
    # 'om_url': 'http://192.168.1.150/xml',  # 给om发送来电转分机，post请求的地址
    'om_url': 'https://fanyuan.tpddns.cn:1888/xml',     # 上海那边的om50,发送来电转分机请求
    'app_record_url': 'http://106.15.44.224/audio/',  # 浏览器获取服务器录音文件的地址
    'om_record_url': 'http://192.168.1.150/mcc/Recorder/',  # om存储录音文件的地址
    'linux_path': '/root/learngit/audio',  # 录音下载到阿里云服务器的路径
    'win_path': 'C:/Users/86177/Documents/GitHub/flaskWeb/audio'  # 录音下载到本地电脑上的路径，也是audio的播放路径
}
