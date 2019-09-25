from sqlalchemy import ForeignKey


from . import db

class Ccompany(db.Model):
    __tablename__ = 'ccompany'

    id = db.Column(db.Integer, primary_key=True)
    nam = db.Column(db.String(50), nullable=False)
    principle_name = db.Column(db.String(10))
    area = db.Column(db.String(50))
    fax = db.Column(db.String(50))
    email = db.Column(db.String(50))
    wechat = db.Column(db.String(50))
    phone = db.Column(db.String(50))


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.ForeignKey('ccompany.id'), index=True)
    number = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(10))
    qq = db.Column(db.String(50))
    wechat = db.Column(db.String(50))
    email = db.Column(db.String(50), server_default=db.FetchedValue())

    ccompany = db.relationship('Ccompany', primaryjoin='Client.cid == Ccompany.id', backref='clients')

