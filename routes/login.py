from flask import (
    request,
    render_template,
    Blueprint,

)
from models.user import User

main = Blueprint('login', __name__)


# 做一个用户和密码的判断
@main.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print('post方式登录')
        name = request.form.get('name')
        number = request.form.get('number')
        password = request.form.get('password')
        user = User.query.filter(User.name == name, User.password == password, User.number == number).first()
        if user:
            return render_template('index.html', name=name)
        else:
            return u'用户名或者密码错误，请确认后重新登录'


# 传输图片
@main.route('/images/<name>')
def img_stream(name):
    path = '/root/learngit/images/' + name
    with open(path, 'rb') as img:
        data = img.read()
        print('传递图片...')
    return data
