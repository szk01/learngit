# 这是一个处理来电转分机的对象
# 下载录音，格式化信息，
# 得到来电号码， 录音名称，分机号
#
from utils import om_config, log
import time, subprocess
from models.record import Call_record, Voice_record, db


class Cdr(object):

    def __init__(self, event):
        self.event = event


    @staticmethod
    def wget_down(url):
        cmd = 'wget -P %s %s --http-user=user --http-password=user' % (
        om_config['audio_path'], url)                       # 从OM的Url上下载到计算机相应的地点om_config['audio_path']
        log('执行shell命令，60s之后下载录音...', cmd)
        time.sleep(60)                                      # 60s之后下载录音
        subprocess.call(cmd, shell=True)                    # 将录音文件下载到服务器的指定文件夹中

    # 添加通话记录到mysql数据库
    @staticmethod
    def sql_addCallRecord(cr, func_time, uid):
        if func_time.time['end_time']:
            log('静态方法，添加通话记录', cr)
            call_record = Call_record(phone=cr['phone'], name=cr['name'], type=cr['type'],
                                      start_time=func_time.time['start_time'], on_time=func_time.time['on_time'],
                                      end_time=func_time.time['end_time'], uid=uid,
                                      )
            db.session.add(call_record)
            log('在数据库加入一条通话记录...')
            db.session.commit()


    @staticmethod
    def sql_addVoiceRecord(vr, uid):
        voice_record = Voice_record(name=vr['name'], url=vr['url'], play_count=vr['play_count'],
                                    down_count=vr['down_count'], uid=uid
                                    )
        db.session.add(voice_record)
        log('在数据库加入一条录音记录...')
        db.session.commit()

    # 判断是否漏接
    def is_lose_incoming(self):
        d_time = self.event.find("Duration")
        if d_time == "0":
            return True
        elif d_time != "0":
            return False

    # 漏接电话之后，发送必要的信息：漏接电话，分机
    def lose_info(self):
        info = {}
        number = self.event.find("CPN").text
        seat = self.event.find("CDPN").text
        info['number'] = number
        info['seat'] = seat
        return info

    # 判断话单的类型
    def cdr_type(self):
        type = self.event.find('Type').text
        return type

    # 通话记录，与数据库交互
    def call_record(self):
        cr = {}
        recording = self.event.find('Recording')
        if recording is not None:
            number = self.event.find('CPN').text                # 电话号码
            pid = self.event.find('CDPN').text
            cr['number'] = number
            cr['name'] = '未知'
            cr['type'] = 1
            cr['pid'] = pid                                     # 分机号

        return cr

    # 录音记录，与数据库交互
    def voice_call(self):
        vr = {}
        recording = self.event.find('Recording')
        if recording is not None:
            v_name = recording.text
            pid = self.event.find('CDPN').text
            vr['name'] = v_name                                     # 录音名
            vr['url'] = 'audio/' + v_name                           # 播放地址
            vr['downPath'] = om_config['om_record_url'] + v_name    # 下载地址
            vr['pid'] = pid
            vr['play_count'] = 0
            vr['down_count'] = 0

        return vr

    # 发送给客户端页面，查询这个话单是属于哪个分机，哪个用户，发送哪个客户端
    def to_webPage(self):
        ws = {}
        recording = self.event.find('Recording')
        if recording is not None:
            number = self.event.find('CPN').text                # 电话号码
            ws['number'] = number
            ws['play'] = 'audio/' + recording.text
            ws['pid'] = self.event.find('CDPN').text            # 分机号

        return ws

