from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for,
)
from models.record import db, Voice_record, Call_record
from models.seat import Seat
import time, json
from utils import log
main = Blueprint('index', __name__)


# 格式化call_record表中的时间戳
def formatted(cs):
    for c in cs:
        st = time.localtime(c.start_time)
        format = '%Y/%m/%d %H:%M:%S'
        c.start_time = time.strftime(format, st)  # 格式化开始时间
        # 打入时间
        ot = time.localtime(c.on_time)
        c.on_time = time.strftime(format, ot)
        # 接通时间
        et = time.localtime(c.end_time)
        c.end_time = time.strftime(format, et)

# 通话记录
@main.route('/call_record')
def page_cr():
    authNumber = request.cookies.get('number')
    log('cookie', request.cookies)
    content = {}
    current_page = request.args.get('page', 1, type=int)  # 从查询字符串获取当前页数  current_page是1
    # 使用cookie进行数据隔离
    if authNumber in '10000':
        pagination = Call_record.query.paginate(current_page, per_page=10)  # 分页对象
    elif authNumber == '10087':
        pagination = Call_record.query.filter_by(uid = 1).paginate(current_page, per_page=10)
    elif authNumber == '10088':
        pagination = Call_record.query.filter_by(uid= 2).paginate(current_page, per_page=10)
    cs = pagination.items  # 当前页数的记录列表
    formatted(cs)
    # for v in cs:
    #     print(v)
    content['pagination'] = pagination
    content['cs'] = cs

    return render_template('callRecord.html', **content)


# 格式录音记录的名称
def v_format(vs):
    for v in vs:
        v.name = v.name[:-7]

# 录音记录，10条记录一个页面
# paginate()查询函数需要两个参数，当前页面和此页面记录数
@main.route('/voice_record')
def page_vr():
    authNumber = request.cookies.get('number')
    log('cookie', request.cookies)
    calls = []
    content = {}
    current_page = request.args.get('page', 1, type=int)                                    # 从查询字符串获取当前页数
    # 管理员登录，显示所有的记录
    if authNumber == '10000':
        pagination = Voice_record.query.paginate(current_page, per_page=10)                     # 分页对象
    elif authNumber == '10087':
        pagination = Voice_record.query.filter_by(uid = 1).paginate(current_page, per_page=10)
    elif authNumber == '10088':
        pagination = Voice_record.query.filter_by(uid = 2).paginate(current_page, per_page=10)

    vs = pagination.items  # 当前页数的记录列表
    v_format(vs)
    # for v in vs:
    #     print(v)
    content['pagination'] = pagination
    content['vs'] = vs

    return render_template('voiceRecord.html', **content)

# 已有的座机表
@main.route('/seat')
def seat():
    content = {}
    seats = Seat.query.all()
    print('打印出分机结果集：', seats)
    content['seats'] = seats
    return render_template('seat.html', **content)


# 删除记录
@main.route('/remove', methods=['POST'])
def remove_voiceReocrd():
    data = request.form.get('data')  # post方式传递json格式字符串
    d = json.loads(data)  # 将str转化成字典
    for id in d.get('data'):
        v = Voice_record.query.get(id)
        print(v)
        db.session.delete(v)
        db.session.commit()
    return 'sucess'


# 添加客户信息页面
@main.route('/addClient', methods=['GET'])
def addclient():
    return render_template('addClient.html')