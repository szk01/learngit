from . import db  # 相对引用，db变量存在于models/__init__.py文件中
from . import login_manager
from flask_login import UserMixin


# class User(db.Model, UserMixin):
#     # 表名默认会将模型名转为小写加下划线的形式
#     # 如：UserModel => user_model
#     # 指定表名
#     # 下面的这些字段都是类字段
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(30))
#     number = db.Column(db.String(255), unique=True)
#     password = db.Column(db.String(255))


# 角色表
class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.ForeignKey('company.id'), nullable=False, index=True, server_default=db.FetchedValue())
    fid = db.Column(db.Integer)
    name = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'), nullable=False)
    create_time = db.Column(db.BigInteger)
    update_time = db.Column(db.BigInteger)
    create_uid = db.Column(db.Integer)

    company = db.relationship('Company', primaryjoin='Role.cid == Company.id', backref='roles')


class Company(db.Model):
    # 公司表
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    c_code = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'))  # 公司代码
    name = db.Column(db.String(255), nullable=False)  # 公司名称
    principal_name = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'), nullable=False)  # 公司负责人
    p_uid = db.Column(db.Integer)  # 负责人账号ID
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    wechat = db.Column(db.String(30), nullable=False)
    site = db.Column(db.String(255))
    create_time = db.Column(db.BigInteger)
    update_time = db.Column(db.BigInteger)
    create_uid = db.Column(db.Integer)


class CompanyPermit(db.Model):
    # 公司权限表
    __tablename__ = 'company_permit'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())  # 状态0正常1停用2过期
    cid = db.Column(db.ForeignKey('company.id'), nullable=False, index=True)  # 外键关联到公司表 所属公司ID
    permit = db.Column(db.String(255))  # 功能权限
    create_time = db.Column(db.BigInteger, nullable=False)
    update_time = db.Column(db.BigInteger)
    over_time = db.Column(db.BigInteger, nullable=False)

    company = db.relationship('Company', primaryjoin='CompanyPermit.cid == Company.id', backref='company_permits')


# 用户表
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.ForeignKey('company.id'), index=True)
    rid = db.Column(db.ForeignKey('role.id'), index=True)
    create_uid = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.Integer)
    name = db.Column(db.String(30), nullable=False)  # 昵称
    number = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'), nullable=False)  # 工号
    password = db.Column(db.String(60), nullable=False)  # 密码
    create_time = db.Column(db.BigInteger)
    update_time = db.Column(db.BigInteger)
    login_ip = db.Column(db.String(20))
    login_time = db.Column(db.BigInteger)

    company = db.relationship('Company', primaryjoin='User.cid == Company.id')
    role = db.relationship('Role', primaryjoin='User.rid == Role.id')
