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


# 得出总时长
# def duration(cs):
#     for c in cs:
#         at = c.end_time - c.start_time
#         format = '%Y/%m/%d %H:%M:%S'
#         at = time.strftime(format, at)
#         return at

# 通话记录 使用ORM，从数据库拿到数据
# @main.route('/call_record')
# def call_record():
#     content = {}
#     call_records = Call_record.query.all()  # 拿到call_records中的所有数据
#     formatted(call_records)  # 格式化时间戳
#     # allTime = duration(call_records)                      # 得出总时长
#     # content['allTime'] = allTime
#     content['call_records'] = call_records  # 加入到content中，将content传到前端页面，让jingjia2模板使用
#     return render_template('callRecord.html', **content)


@main.route('/call_record')
def page_cr():
    content = {}
    current_page = request.args.get('page', 1, type=int)  # 从查询字符串获取当前页数
    # per_page = current_app.config['BLUELOG_POST_PER_PAGE']  # 每页数量
    pagination = Call_record.query.paginate(current_page, per_page=12)  # 分页对象
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


# # 录音记录
# @main.route('/voice_record')
# def voice_record():
#     content = {}
#     voice_records = Voice_record.query.all()
#     v_format(voice_records)
#     content['voice_records'] = voice_records
#     return render_template('voiceRecord.html', **content)


# 通话记录，10条记录一个页面
# paginate()查询函数需要两个参数，当前页面和此页面记录数
@main.route('/voice_record')
def page_vr():
    content = {}
    current_page = request.args.get('page', 1, type=int)  # 从查询字符串获取当前页数
    # per_page = current_app.config['BLUELOG_POST_PER_PAGE']  # 每页数量
    pagination = Voice_record.query.paginate(current_page, per_page=10)  # 分页对象
    vs = pagination.items  # 当前页数的记录列表
    v_format(vs)
    # for v in vs:
    #     print(v)
    content['pagination'] = pagination
    content['vs'] = vs

    return render_template('voiceRecord.html', **content)


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