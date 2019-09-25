'''
坐席表暂时先不用
'''
from sqlalchemy import ForeignKey


from . import db
class Seat(db.Model):
    __tablename__ = 'seat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, ForeignKey('user.id'))                  # 外键，关联到用户表
    number = db.Column(db.String(255), unique=True)                     # 座机号码，比如212
    bind_time = db.Column(db.Integer)                                   # 用户登录最后的时间，使用时间戳


