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

# 这些都是显示用户信息
@main.route('/manage_account', methods=['GET'])
def manageAccount():
    userInfo = {}
    # log('cookie', request.cookies.get('number'))
    # number = request.cookies.get('number')
    number = session['number']
    log('account session', number)
    user = User.query.filter_by(number=number).first()
    userInfo['user_name'] = user.name
    userInfo["user_number"] = user.number
    role = user.rid
    if role == 1 :
        userInfo["user_role"] = '客服'
    elif role == 2:
        userInfo["user_role"] = '管理员'

    # 拿到账号对应的分机号码
    uid = user.id
    seat = Seat.query.filter_by(uid=uid).first()
    userInfo['user_seat'] = seat.number

    return render_template('manage_account.html', **userInfo)

# 更新密码
@main.route('/change_password', methods=['POST'])
def changePassword():
    form = request.form
    account = form.get('account')
    log('form', account)
    user = User.query.filter_by(number=account).first()
    user.password = form.get('password')
    db.session.commit()
    return 'sucess'

# 验证管理员身份，创建用户
@main.route('/creat_user', methods=['POST', 'GET'])
def creatUser():
    authNumber = session['number']
    log('creatUser authNumber', authNumber)
    # 如果是管理员权限，可以创建一个用户
    if authNumber == '10000':
        form = request.form
        log('form', form)
        # 创建一个用户    orm对应的class，操作一个对象即可

    return '123'