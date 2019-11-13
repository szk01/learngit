# # coding: utf-8
# from sqlalchemy import BigInteger, Column, Float, ForeignKey, Integer, String
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
#     uid = db.Column(db.ForeignKey('user.id'), index=True)
#     phone = db.Column(db.String(30), nullable=False)
#     name = db.Column(db.String(30, 'utf8_bin'))
#     type = db.Column(db.Integer, nullable=False)
#     start_time = db.Column(db.Integer, nullable=False)
#     on_time = db.Column(db.Integer)
#     end_time = db.Column(db.Integer)
#
#     user = db.relationship('User', primaryjoin='CallRecord.uid == User.id', backref='call_records')
#
#
# class Ccompany(db.Model):
#     __tablename__ = 'ccompany'
#
#     id = db.Column(db.Integer, primary_key=True)
#     c_code = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     name = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False)
#     phone = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
#     email = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     area = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
#     main_class = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     type = db.Column(db.String(255))
#     banker = db.Column(db.String(50, 'utf8mb4_es_0900_ai_ci'))
#     industry = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     route_range = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     client_source = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     platform = db.Column(db.String(50))
#     address = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
#     ct = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     ut = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     client_code = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     qq = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     main_route = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     url = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     department = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))
#     contact_name = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     contact_sex = db.Column(db.String(2, 'utf8mb4_0900_ai_ci'))
#     contact_unit_phone = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     contact_fax = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     contact_phone = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     contact_msn = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     contact_c_email = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     contact_p_email = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     contact_add = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
#     contact_postal_code = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     contact_role = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     contact_qq = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#
#
# class Ccompany1(db.Model):
#     __tablename__ = 'ccompany1'
#
#     id = db.Column(db.Integer, primary_key=True)
#     u_id = db.Column(db.Integer)
#     c_code = db.Column(db.String(20))
#     name = db.Column(db.String(255))
#     phone = db.Column(db.String(50))
#     address = db.Column(db.String(255))
#     industry = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
#     route_range = db.Column(db.String(255))
#     principal_name = db.Column(db.String(15))
#
#
# class Client(db.Model):
#     __tablename__ = 'client'
#
#     id = db.Column(db.Integer, primary_key=True)
#     clid = db.Column(db.Integer, index=True)
#     cid = db.Column(db.Integer, index=True)
#     number = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
#     name = db.Column(db.String(10))
#     qq = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     wechat = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     email = db.Column(db.String(50), server_default=db.FetchedValue())
#
#
# class Client1(db.Model):
#     __tablename__ = 'client1'
#
#     id = db.Column(db.Integer, primary_key=True)
#     com_id = db.Column(db.ForeignKey('ccompany1.id'), index=True)
#     name = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
#     sex = db.Column(db.String(11))
#     phone = db.Column(db.String(50))
#     email = db.Column(db.String(255))
#     position = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     qq = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#
#     com = db.relationship('Ccompany1', primaryjoin='Client1.com_id == Ccompany1.id', backref='client1s')
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
#     update_time = db.Column(db.BigInteger)
#
#     role = db.relationship('Role', primaryjoin='RolePermit.rid == Role.id', backref='role_permits')
#
#
# class Seat(db.Model):
#     __tablename__ = 'seat'
#
#     id = db.Column(db.Integer, primary_key=True)
#     uid = db.Column(db.ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
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
#     clid = db.Column(db.ForeignKey('client.id'), index=True)
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
#     phone = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'), server_default=db.FetchedValue())
#
#     company = db.relationship('Company', primaryjoin='User.cid == Company.id')
#     client = db.relationship('Client', primaryjoin='User.clid == Client.id')
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
# class VoiceRecord(db.Model):
#     __tablename__ = 'voice_record'
#
#     id = db.Column(db.Integer, primary_key=True)
#     uid = db.Column(db.ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
#     name = db.Column(db.String(255), nullable=False)
#     url = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False)
#     play_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#     down_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#
#     user = db.relationship('User', primaryjoin='VoiceRecord.uid == User.id', backref='voice_records')
