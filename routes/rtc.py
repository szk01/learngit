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

import hashlib, uuid, datetime, time, json
from optparse import OptionParser

main = Blueprint('rtc', __name__)


parser = OptionParser()
parser.add_option("-a", "--listen", dest="listen", help="Listen port")
parser.add_option("-d", "--appid", dest="appID", help="ID of app")
parser.add_option("-k", "--appkey", dest="appKey", help="Key of app")
parser.add_option("-e", "--gslb", dest="gslb", help="URL of GSLB")

(options, args) = parser.parse_args()
(listen, app_id, app_key, gslb) = (options.listen, options.appID, options.appKey, options.gslb)

'''
客服端发送过来的参数有：
    
'''


# 创建user_id
def create_user_id(channel_id, user):
    h = hashlib.sha256()
    h.update(channel_id)
    h.update('/')
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
    h.update(str(timestamp))
    token = h.hexdigest()
    return token


# 将get的查询参数组成字典
def all_querys(args):
    query_list =  args.items().__str__()
    query_dict = {}
    for query in query_list:
        query_dict[query[0]] = query[1]
    return query_dict


# 首页
@main.route('/rtc')
def index():
    return render_template('rtc.html')

# ajax请求
@main.route('/app/v1/login')
def rtc():
    querys = all_querys(request.args)
    channel_id = querys.get("room")
    user_id = create_user_id(channel_id, querys.get("user"))
    nonce = "AK-%s" % str(uuid.uuid4())
    expire = datetime.datetime.now() + datetime.timedelta(days=2)  # expire 到期
    timestamp = int(time.mktime(expire.timetuple()))
    token = create_token(app_id, app_key, querys.get("room"), user_id, nonce, timestamp)

    username = "%s?appid=%s&channel=%s&nonce=%s&timestamp=%d" % (
        user_id, app_id, channel_id, nonce, timestamp
    )

    ret = json.dumps({"code": 0, "data": {
        "appid": app_id, "userid": user_id, "gslb": [gslb],
        "token": token, "nonce": nonce, "timestamp": timestamp,
        "turn": {
            "username": username,
            "password": token
        }
    }})
    response = make_response(ret)
    response.headers["Content-Type"] = "application/json"
    return response

# AppKey：dde07e3682c1ea002a70a2d7d743edbd