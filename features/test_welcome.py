from utils import log, post_om


def welcome(vid):
    # 发送语音评价
    s_body = '<Transfer attribute="Connect"><visitor id="%s" /><menu id="6"/></Transfer>' % vid
    log('播放欢迎词')
    post_om(s_body)