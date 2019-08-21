from flask import (
    request,
    render_template,
    Blueprint,

)
from models.user import User

main = Blueprint('login', __name__)

room = {
    "215": None,
    "216": None
}

# 做一个用户和密码的判断
@main.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print('post方式登录')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            return render_template('test.html', ip=username)
        else:
            return u'用户名或者密码错误，请确认后重新登录'
