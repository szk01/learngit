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
    else:
        print('post方式登录')
        name = request.form.get('name')
        number = request.form.get('number')
        password = request.form.get('password')
        user = User.query.filter(User.name == name, User.password == password, User.number == number).first()
        if user:
            # return render_template('index.html', name=name)
            return redirect(url_for("index"))
        else:
            return u'用户名或者密码错误，请确认后重新登录'


@main.route('/index', methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return '必须先登录'
    else:
        return render_template('index.html')


# 传输图片
@main.route('/images/<name>')
def img_stream(name):
    win_path = 'C:/Users/86177/Documents/GitHub/flaskWeb/images/' + name
    # path = '/root/learngit/images/' + name
    with open(win_path, 'rb') as img:
        data = img.read()
        print('传递图片...')
    return data
