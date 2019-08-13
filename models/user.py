from flask_sqlalchemy import SQLAlchemy
from app import app
from sqlalchemy import Column, Integer, String

# 创建数据库操作对象
db = SQLAlchemy(app)
# 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名test
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost:3306/test'
# 设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class User(db.Model):
    # 表名默认会将模型名转为小写加下划线的形式
    # 如：UserModel => user_model
    # 指定表名
    # 下面的这些字段都是类字段
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, name, password):
        self.name = name
        self.password = password