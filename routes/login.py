from flask import (
    Flask,
    request,
    render_template,
)
from app import app
from models.user import User


# 做一个用户和密码的判断
@app.route('/login', methods=['POST'])
def login():
    form = request.form
    name = form['username']
    pwd = form['password']
    user = User.query.filter_by(username=name).first()
    if user.password == pwd:
        return render_template("index.html")        # 登录成功
    else:
        return render_template("login.html", status="用户名或者密码错误")    # 登录失败

