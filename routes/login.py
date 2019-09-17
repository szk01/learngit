from flask import (
    request,
    render_template,
    Blueprint,
    redirect,
    url_for
)
from models.user import User

main = Blueprint('login', __name__)


# 做一个用户和密码的判断
# 重定向到首页
@main.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    # else:
    #     print('post方式登录')
    #     name = request.form.get('name')
    #     number = request.form.get('number')
    #     us['number'] = number
    #     password = request.form.get('password')
    #     user = User.query.filter(User.name == name, User.password == password, User.number == number).first()
    #     if user:
    #         print(number)
    #         return render_template('index.html', number=number)
    #     else:
    #         return u'用户名或者密码错误，请确认后重新登录'


@main.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # 重定向到login登录页面，不明白为什么是.login，算是保护路由
        return redirect(url_for('.login'))
    else:
        print('post方式登录')
        name = request.form.get('name')
        number = request.form.get('number')
        password = request.form.get('password')
        user = User.query.filter(User.name == name, User.password == password, User.number == number).first()
        if user:
            print(number)
            return render_template('index.html', number=number)
        else:
            return u'用户名或者密码错误，请确认后重新登录'
