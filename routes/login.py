from flask import (
    request,
    render_template,
    Blueprint
)
from models.user import User

main1 = Blueprint('login', __name__)

# 做一个用户和密码的判断
@main.route('/login', methods=['POST'])
def login():
    form = request.form
    name = form['username']
    pwd = form['password']
    user = User.query.filter_by(username=name).first()
    if user.password == pwd:
        return render_template("index.html")        # 登录成功
    else:
        return render_template("login.html", status="用户名或者密码错误")    # 登录失败

