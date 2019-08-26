# coding: utf-8
# from sqlalchemy import BigInteger, Column, Float, ForeignKey, Integer, String, Table
# from sqlalchemy.orm import relationship
# from sqlalchemy.schema import FetchedValue
# from flask_sqlalchemy import SQLAlchemy
#
#
# db = SQLAlchemy()
#
#
# class CallRecord(db.Model):
#     __tablename__ = 'call_record'
#
#     id = db.Column(db.Integer, primary_key=True)
#     uid = db.Column(db.ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
#     phone = db.Column(db.String(30), nullable=False)
#     name = db.Column(db.String(30))
#     type = db.Column(db.Integer, nullable=False)
#     start_time = db.Column(db.Integer, nullable=False)
#     on_time = db.Column(db.Integer)
#     end_time = db.Column(db.Integer)
#
#     user = db.relationship('User', primaryjoin='CallRecord.uid == User.id', backref='call_records')
#
#
# class Company(db.Model):
#     __tablename__ = 'company'
#
#     id = db.Column(db.Integer, primary_key=True)
#     c_code = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'))
#     name = db.Column(db.String(255), nullable=False)
#     principal_name = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'), nullable=False)
#     p_uid = db.Column(db.Integer)
#     phone = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(20), nullable=False)
#     wechat = db.Column(db.String(30), nullable=False)
#     site = db.Column(db.String(255))
#     create_time = db.Column(db.BigInteger)
#     update_time = db.Column(db.BigInteger)
#     create_uid = db.Column(db.Integer)
#
#
# class CompanyPermit(db.Model):
#     __tablename__ = 'company_permit'
#
#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#     cid = db.Column(db.ForeignKey('company.id'), nullable=False, index=True)
#     permit = db.Column(db.String(255))
#     create_time = db.Column(db.BigInteger, nullable=False)
#     update_time = db.Column(db.BigInteger)
#     over_time = db.Column(db.BigInteger, nullable=False)
#
#     company = db.relationship('Company', primaryjoin='CompanyPermit.cid == Company.id', backref='company_permits')
#
#
# class Power(db.Model):
#     __tablename__ = 'power'
#
#     id = db.Column(db.Integer, primary_key=True)
#     fid = db.Column(db.Integer, nullable=False)
#     type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#     status = db.Column(db.Integer, nullable=False)
#     name = db.Column(db.String(30), nullable=False)
#     url = db.Column(db.String(100))
#     price = db.Column(db.Float(6), nullable=False)
#     create_time = db.Column(db.BigInteger, nullable=False)
#     update_time = db.Column(db.BigInteger)
#
#
# class Role(db.Model):
#     __tablename__ = 'role'
#
#     id = db.Column(db.Integer, primary_key=True)
#     cid = db.Column(db.ForeignKey('company.id'), nullable=False, index=True, server_default=db.FetchedValue())
#     fid = db.Column(db.Integer)
#     name = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'), nullable=False)
#     create_time = db.Column(db.BigInteger)
#     update_time = db.Column(db.BigInteger)
#     create_uid = db.Column(db.Integer)
#
#     company = db.relationship('Company', primaryjoin='Role.cid == Company.id', backref='roles')
#
#
# class RolePermit(db.Model):
#     __tablename__ = 'role_permit'
#
#     id = db.Column(db.Integer, primary_key=True)
#     rid = db.Column(db.ForeignKey('role.id'), nullable=False, index=True)
#     permit = db.Column(db.String(255))
#     update_time = db.Column(db.BigInteger, nullable=False)
#
#     role = db.relationship('Role', primaryjoin='RolePermit.rid == Role.id', backref='role_permits')
#
#
# class Seat(db.Model):
#     __tablename__ = 'seat'
#
#     id = db.Column(db.Integer, primary_key=True)
#     uid = db.Column(db.ForeignKey('user.id'), nullable=False, index=True)
#     number = db.Column(db.String(30), nullable=False)
#     bind_time = db.Column(db.Integer)
#
#     user = db.relationship('User', primaryjoin='Seat.uid == User.id', backref='seats')
#
#
# class User(Base):
#     __tablename__ = 'user'
#
#     id = db.Column(db.Integer, primary_key=True)
#     cid = db.Column(db.ForeignKey('company.id'), index=True)
#     rid = db.Column(db.ForeignKey('role.id'), index=True)
#     create_uid = db.Column(db.Integer)
#     status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#     type = db.Column(db.Integer)
#     name = db.Column(db.String(30), nullable=False)
#     number = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'), nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     create_time = db.Column(db.BigInteger)
#     update_time = db.Column(db.BigInteger)
#     login_ip = db.Column(db.String(20))
#     login_time = db.Column(db.BigInteger)
#
#     company = db.relationship('Company', primaryjoin='User.cid == Company.id')
#     role = db.relationship('Role', primaryjoin='User.rid == Role.id')
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False)
#     number = db.Column(db.String(255), nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#
#
# t_voice_record = db.Table(
#     'voice_record',
#     db.Column('id', db.Integer, nullable=False, index=True),
#     db.Column('record_id', db.ForeignKey('call_record.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True),
#     db.Column('name', db.String(255), nullable=False),
#     db.Column('url', db.String(255), nullable=False),
#     db.Column('play_count', db.Integer, nullable=False, server_default=db.FetchedValue()),
#     db.Column('down_count', db.Integer, nullable=False, server_default=db.FetchedValue())
# )
