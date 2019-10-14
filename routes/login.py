from flask import (
    request,
    render_template,
    Blueprint,
    redirect,
    url_for,
    make_response,
    session,
)
from models.user import User
from utils import log

main = Blueprint('login', __name__)


# 重定向到首页
@main.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


# 登录 根据用户的不同给予不同的数据
@main.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # 重定向到login登录页面，不明白为什么是.login，算是保护路由
        return redirect(url_for('.login'))
    else:
        print('post方式登录')
        number = request.form.get('number')
        password = request.form.get('password')
        log('n p', number, password)
        user = User.query.filter_by(password=password, number=number).first()
        log('user', user)
        if user:
            print(number)
            # response = make_response(render_template('index.html', number=number))
            # response.set_cookie('number', number)
            # return response
            session['number'] = number
            return render_template('index.html', number=number)
        else:
            return u'用户名或者密码错误，请确认后重新登录'


