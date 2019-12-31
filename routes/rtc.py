from flask import (
    Blueprint,
    render_template,
    request,
    make_response,
    jsonify,
    redirect,
    session,
    url_for,
)
from models.client import db, Client1
from models.ccompany import Ccompany1

from utils import log, serialize
import copy

import hashlib, uuid, datetime, time, json, os
from optparse import OptionParser

main = Blueprint('rtc', __name__)

parser = OptionParser()
# parser.add_option("-a", "--listen", dest="listen", help="Listen port")
# parser.add_option("-d", "--appid", dest="zk46xnwd", help="ID of app")
# parser.add_option("-k", "--appkey", dest="dde07e3682c1ea002a70a2d7d743edbd", help="Key of app")
# parser.add_option("-e", "--gslb", dest="gslb", help="URL of GSLB")
#
# (options, args) = parser.parse_args()
# # (listen, app_id, app_key, gslb) = (options.listen, options.appID, options.appKey, options.gslb)
# (app_id, app_key, gslb) = (options.appID, options.appKey, options.gslb)

app_id = 'zk46xnwd'.encode('utf-8'),
app_key = 'dde07e3682c1ea002a70a2d7d743edbd'.encode('utf-8'),

'''
客服端发送过来的参数有：
    
'''


class PublisherInfo(object):
    pInfo = {}

    def removePub(self, userId):
        p = PublisherInfo.pInfo.get(userId)
        PublisherInfo.pInfo.pop(p)

    def addPub(self, pub):
        pub = json.loads(pub)
        PublisherInfo.pInfo.update(pub)



class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


# 创建user_id
def create_user_id(channel_id, user):
    h = hashlib.sha256()
    h.update(channel_id)
    h.update('/'.encode('utf-8'))
    h.update(user)
    uid = h.hexdigest()
    return str(uid[0:16])


# 创建token
def create_token(app_id, app_key, channel_id, user_id, nonce, timestamp):
    h = hashlib.sha256()
    h.update(app_id)
    h.update(app_key)
    h.update(channel_id)
    h.update(user_id)
    h.update(nonce)
    h.update(str(timestamp).encode('utf-8'))
    token = h.hexdigest()
    return token


# 将get的查询参数组成字典
def all_querys(args):
    query_list = args.items().__str__()
    query_dict = {}
    for query in query_list:
        query_dict[query[0]] = query[1]
    return query_dict


# 首页
@main.route('/rtc', methods=['POST', 'GET'])
def index():
    return render_template('rtc.html')


# ajax请求
@main.route('/app/v1/login', methods=['POST', 'GET'])
def rtc():
    data = request.form
    log('data', data)
    channel_id = data.get("room").encode('utf-8')
    log('channel_id', channel_id, type(channel_id))
    user = data.get("user").encode('utf-8')
    user_id = create_user_id(channel_id, user).encode('utf-8')
    nonce = "AK-%s" % str(uuid.uuid4())
    expire = datetime.datetime.now() + datetime.timedelta(days=2)  # expire 到期
    timestamp = int(time.mktime(expire.timetuple()))
    token = create_token('zk46xnwd'.encode('utf-8'), 'dde07e3682c1ea002a70a2d7d743edbd'.encode('utf-8'), channel_id,
                         user_id, nonce.encode('utf-8'), timestamp)

    username = "%s?appid=%s&channel=%s&nonce=%s&timestamp=%d" % (
        user_id, app_id, channel_id, nonce, timestamp
    )

    ret = json.dumps({"code": 0, "data": {
        "appid": app_id, "userid": user_id, "gslb": ["https://rgslb.rtc.aliyuncs.com"],
        "token": token, "nonce": nonce, "timestamp": timestamp,
        "turn": {
            "username": username,
            "password": token,
        }
    }}, cls=MyEncoder, indent=4)
    log("ret", ret)
    response = make_response(ret)
    response.headers["Content-Type"] = "application/json"
    return response


# ajax共享屏幕请求
@main.route('/app/v1/screenTrack')
def screenTrack():
    querys = all_querys(request.args)
    channel_id = querys.get("room")
    user_id = create_user_id(channel_id, querys.get("user"))

    ret = json.dumps({"code": 101, "data": {
        "userId": user_id, "label": "sophon_video_screen_share",
    }})
    response = make_response(ret)
    response.headers["Content-Type"] = "application/json"
    return response


# ajax的上传发布流的人数
@main.route('/upload/Publisher', methods=['POST'])
def publisherInfo():
    data = request.form
    log('上传到服务器', data)
    pub = PublisherInfo()
    pub.addPub(json.loads(data))
    log('服务器中发布流的信息', publisherInfo)
    return 'upload success'


# ajax 取得上传发布流的人数
@main.route('/get/Publisher', methods=['POST'])
def getPublisher():
    data = json.dumps(publisherInfo)
    log('存在的发布流的人', data)
    return data


# AppKey：dde07e3682c1ea002a70a2d7d743edbd

basedir = os.path.abspath(os.path.dirname(__file__))    # 获取当前项目的绝对路径
ALLOWED_EXTENSIONS = set(['txt', 'png', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF', 'pdf', 'PDF'])   # 允许上传的文件后缀


# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.spilt('.', 1)[1] in ALLOWED_EXTENSIONS


# 上传文件
@main.route('/api/upload', methods=['POST'])
def uploadFile():
    log('basedir', basedir)
    file_dir = os.path.join(basedir, 'upload_file')
    log("保存文件的文件夹", file_dir)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']
    log('上传文件的名称', f)
    if f and allowed_file(f.filename):
        fname = f.filename
        ext = fname.spilit('.', 1)[1]                  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext      # 修改文件名
        log('上传的文件', new_filename)
        f.save(os.path.join(file_dir, new_filename))    # 保存文件到upload目录

        return jsonify({"status": "error", "msg": "上传成功"})
    else:
        return jsonify({"status": "success", "msg": "上传失败"})







