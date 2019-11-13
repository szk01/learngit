from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
import time, json
from utils import log
from models.user import User, db
from models.seat import Seat

main = Blueprint('account', __name__)


# 在user表中加入一条记录，添加一条记录
def add_user(account, username, password, gs, role, phone):
    # 判断所属的角色
    rid = 1
    if role == "Customer_service":
        rid = 1
    elif role == "operating":
        rid = 3
    elif role == "kefu_manager":
        rid = 4
    # 判断所属公司的id
    cid = 1
    if gs == "shanghai":
        cid = 2
    elif gs == "yuanan":
        cid = 3
    elif gs == "congzuo":
        cid = 4
    user = User(number=account, name=username, password=password, status=1, cid=cid, rid=rid, phone=phone)
    db.session.add(user)
    log('添加一个用户...')
    db.session.commit()


# 在seat表中添加一个座机记录，添加一个座机
def add_seat(seat, number):
    # 通过外键找到对应的用户
    user = User.query.filter_by(number=number).first()
    uid = user.id
    seat = Seat(number=seat, uid=uid)
    db.session.add(seat)
    log('添加一个座机...')
    db.session.commit()


# 整个页面的路由
@main.route('/manage_account', methods=['GET'])
def manageAccount():
    userInfo = {}
    number = session.get('number')
    log('account session', number)
    user = User.query.filter_by(number=number).first()
    userInfo['user_name'] = user.name
    userInfo["user_number"] = user.number

    role = user.rid
    if role == 1:
        userInfo["user_role"] = '客服'
        log('登录的是客服')
        uid = user.id
        seat = Seat.query.filter_by(uid=uid).first()
        if seat:  # 找到客服的分配的分机
            userInfo['user_seat'] = seat.number
        return render_template('manage_account.html', **userInfo)

    elif role == 2:
        userInfo["user_role"] = '管理员'
        log('登录的是管理员')
        userInfo['user_seat'] = ""
        # 用户信息分页，只在管理员页面才有的路由
        current_page = request.args.get('page', 1, type=int)
        pagination = User.query.paginate(current_page, per_page=10)
        users = pagination.items
        log('user', users)
        userInfo['users'] = users
        userInfo['pagination'] = pagination
        return render_template('admin_account.html', **userInfo)

    # 拿到账号对应的分机号码


# ajax 更新密码
@main.route('/change_password', methods=['POST'])
def changePassword():
    form = request.form
    account = form.get('account')
    log('form', account)
    user = User.query.filter_by(number=account).first()
    user.password = form.get('password')
    db.session.commit()
    return 'sucess'


# ajax验证管理员身份，创建用户
@main.route('/create_user', methods=['POST', 'GET'])
def creatUser():
    authNumber = session['number']
    log('creatUser authNumber', authNumber)
    # 如果是管理员权限，可以创建一个用户
    if authNumber == '10000':
        form = request.form
        account = form.get("account")
        username = form.get("username")
        password = form.get("password")
        seat = form.get("seatNumber")
        gs = form.get("gs")
        role = form.get("role")
        phone = form.get("phone")
        # 先添加用户， 再添加分机
        add_user(account, username, password, gs, role, phone)
        add_seat(seat, account)
        log('form', form)
        # 创建一个用户    orm对应的class，操作一个对象即可
        return 'create sucess'

    return 'you have no permission'


# ajax
def singal_user(Model):
    log('Model', type(Model))
    user_info = dict(
        id=Model.id,
        account=Model.number,
        name=Model.name,
        gs=Model.company.name,
        status=Model.status,
        role=Model.role.name,
        phone=Model.phone,
    )
    id = Model.id
    number = ""
    seat = Seat.query.filter_by(uid=int(id)).first()
    if seat:
        number = seat.number

    user_info['seat'] = number

    return user_info


# 用户信息，分页操作
@main.route('/user/list', methods=["POST, GET"])
def all_users():
    userInfo = {}
    number = session['number']
    log('account session', number)
    user = User.query.filter_by(number=number).first()
    userInfo['user_name'] = user.name
    userInfo["user_number"] = user.number

    role = user.rid

    if role == 1:
        userInfo["user_role"] = '管理员'
        log('登录的是管理员')
        userInfo['user_seat'] = ""
        # 用户信息分页，只在管理员页面才有的路由
        current_page = request.args.get('page', 1, type=int)
        pagination = User.query.paginate(current_page, per_page=5)
        users = pagination.items
        log('user', users)
        userInfo['users'] = users
        return render_template('admin_account.html', **userInfo)


# ajax 更新用户信息
@main.route('/update/user_info', methods=["POST", "GET"])
def update_user_info():
    userNumber = session['number']
    if userNumber != '10000':
        form = request.form
        user_name = form.get("user_name")
        password = form.get("password")
        phone = form.get("phone")
        data_seat = form.get("seat")
        # 在User表中找到对应的用户记录,然后跟新记录
        # 在Seat表中找到对应的座机记录，然后更新分机号
        user = User.query.filter_by(number=userNumber).first()
        # 更新这条user记录
        user.name = user_name
        user.password = password
        user.phone = phone
        log('信息更新成功', form)
        db.session.commit()
        # 更新这条seat记录
        uid = user.id
        seat = Seat.query.filter_by(uid=uid).first()
        seat.number = data_seat
        db.session.commit()
        return 'sucess'


# ajax admin删除一个用户，及其对应的分机
@main.route('/delete/user', methods=['POST', 'GET'])
def remove_user():
    form = request.form
    log('form', form)
    id = form.get("id")
    # 清除对应分机的uid
    seat = Seat.query.filter_by(uid=int(id)).first()
    seat.uid = None
    db.session.commit()
    # 再删除对应的用户（再删除主键）
    user = User.query.filter_by(id=int(id)).first()
    db.session.delete(user)
    log('删除对应的分机和用户')
    db.session.commit()

    return 'delete success'


# 更新用户表中的某个用户信息
@main.route('/update/user', methods=['POST', 'GET'])
def update_user():
    data = request.form
    log('data, update/user', data)
    id = data.get('id')
    seat = data.get('seat')
    # 更新用户表的信息
    user = User.query.filter_by(id=int(id)).first()
    user.number = data.get('account')
    user.name = data.get('name')
    user.status = int(data.get('status'))
    user.cid = int(data.get('gs'))
    user.rid = int(data.get('role'))
    log('role', data.get('role'))
    user.phone = data.get('phone')
    db.session.commit()

    seat = Seat.query.filter_by(number=seat).first()
    if seat:
        seat.uid = int(id)
        db.session.commit()
    elif seat == 'None':
        return 'seat none'

    return 'update success'


