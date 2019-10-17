from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for,
    jsonify,
)
from models.record import db, Voice_record, Call_record
from models.user import User
from models.seat import Seat
import time, json
from utils import log
from allFuncs import Funcs

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
        log('c', c.end_time)

# 通话记录
@main.route('/call_record')
def page_cr():
    authNumber = session['number']
    log('session', authNumber)
    content = {}
    current_page = request.args.get('page', 1, type=int)  # 从查询字符串获取当前页数  current_page是1
    global pagination
    log('查询参数', current_page)

    if authNumber == '10000':  # 如果是管理员登录
        pagination = Call_record.query.paginate(current_page, per_page=10)  # 分页对象

    else:  # 如果是客服登录
        user = User.query.filter_by(number=authNumber).first()
        pagination = Call_record.query.filter_by(uid=user.id).paginate(current_page, per_page=10)

    cs = pagination.items  # 当前页数的记录列表
    formatted(cs)  # 格式化时间戳
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
    authNumber = session['number']
    log('cookie voice', authNumber)
    content = {}
    current_page = request.args.get('page', 1, type=int)  # 从查询字符串获取当前页数
    global pagination


    # 如果用户存在，找到对应的录音文件
    if authNumber == '10000':
        pagination = Voice_record.query.paginate(current_page, per_page=10)                     # 分页对象

    else:
        user = User.query.filter_by(number=authNumber).first()
        pagination = Voice_record.query.filter_by(uid = user.id).paginate(current_page, per_page=10)


    vs = pagination.items  # 当前页数的记录列表
    v_format(vs)

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


# 返回分机状态
@main.route('/seat_status', methods=['POST'])
def status():
    '''
    p = {
        'BUSY': set(),
        'IDLE': {'213'},                    # 当前端页面设置了分机的优先级，使用此分机进行测试
        'ONLINE': {'213'},
        'OFFLINE': set(),
        'pid': '213',                         # 写死的默认分机，前端没有设置分机优先的时候，使用此分机
        'priority': {                      # 这是默认优先级，数字越小，优先级越高。这些数据并没有用，只是前台设置后的demo示例
            '212': 1,
            '213': 2,
            '214': 3,
        }
    }
    '''
    data = {}
    busy = Funcs.p['BUSY']
    for b in busy:                          # busy是{'213', '214'} 这种集合
        data[b] = 'busy'

    idle = Funcs.p['IDLE']
    for i in idle:                          # busy是{'213', '214'} 这种集合
        data[i] = 'idle'

    online = Funcs.p['ONLINE']
    for o in online:                        # busy是{'213', '214'} 这种集合
        data[o] = 'online'

    log('data', data)
    return jsonify(data)


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