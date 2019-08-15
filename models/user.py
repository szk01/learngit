from . import db                        # 相对引用


class User(db.Model):
    # 表名默认会将模型名转为小写加下划线的形式
    # 如：UserModel => user_model
    # 指定表名
    # 下面的这些字段都是类字段
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

