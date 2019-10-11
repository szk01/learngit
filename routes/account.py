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

    if number == '10087':
        userInfo["user_seat"] = '213'
    elif number == '10088':
        userInfo["user_seat"] = '214'
    elif number == '10089':
        userInfo["user_seat"] = '215'                  # 工号

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