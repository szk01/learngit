from sqlalchemy import ForeignKey

from . import db  # 相对引用，db变量存在于models/__init__.py文件中
import time


class Voice_record(db.Model):
    __tablename__ = 'voice_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, ForeignKey('user.id'))
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))  # 下载url
    play_count = db.Column(db.Integer)  # 播放次数
    down_count = db.Column(db.Integer)  # 下载次数


class Call_record(db.Model):
    # 表名默认会将模型名转为小写加下划线的形式
    # 如：UserModel => user_model
    # 指定表名
    # 下面的这些字段都是类字段
    __tablename__ = 'call_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, ForeignKey('user.id'))
    phone = db.Column(db.String(30))  # 来电号码
    name = db.Column(db.String(30))  # 来电人姓名
    type = db.Column(db.Integer)  # 电话记录的类型
    start_time = db.Column(db.Integer)  # 电话打进的时间
    on_time = db.Column(db.Integer)  # 电话接入的时间
    end_time = db.Column(db.Integer)  # 通话结束时间

    user = db.relationship('User', primaryjoin='Call_record.uid == User.id', backref='call_records')



