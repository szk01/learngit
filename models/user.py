from . import db  # 相对引用，db变量存在于models/__init__.py文件中
from . import login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    # 表名默认会将模型名转为小写加下划线的形式
    # 如：UserModel => user_model
    # 指定表名
    # 下面的这些字段都是类字段
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    number = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))


class User2(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.ForeignKey('company.id'), index=True)
    rid = db.Column(db.ForeignKey('role.id'), index=True)
    create_uid = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.Integer)
    name = db.Column(db.String(30), nullable=False)
    number = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    create_time = db.Column(db.BigInteger)
    update_time = db.Column(db.BigInteger)
    login_ip = db.Column(db.String(20))
    login_time = db.Column(db.BigInteger)

    company = db.relationship('Company', primaryjoin='User.cid == Company.id')
    role = db.relationship('Role', primaryjoin='User.rid == Role.id')


@login_manager.user_loader
# user_loader是一个回调函数，
def load_user(user_id):
    return User.query.get(int(user_id))
