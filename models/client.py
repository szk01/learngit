from sqlalchemy import ForeignKey


from . import db


class Client1(db.Model):
    __tablename__ = 'client1'

    id = db.Column(db.Integer, primary_key=True)
    com_id = db.Column(db.ForeignKey('ccompany1.id'), index=True)
    name = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    sex = db.Column(db.String(11))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(255))
    position = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
    qq = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))

    com = db.relationship('Ccompany1', primaryjoin='Client1.com_id == Ccompany1.id', backref='client1s')


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    # cid = db.Column(db.ForeignKey('ccompany.id'), index=True)
    clid = db.Column(db.ForeignKey('user.id'), index=True)
    number = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(10))
    qq = db.Column(db.String(50))
    wechat = db.Column(db.String(50))
    email = db.Column(db.String(50), server_default=db.FetchedValue())

    # ccompany = db.relationship('Ccompany', primaryjoin='Client.cid == Ccompany.id', backref='clients')
    user = db.relationship('User', primaryjoin='Client.clid == User.id', backref='clients')

    # 实例化对象后，使用的函数
    # 实例 client = Client.query.filter_by(...)
    # client.logId()， self是client实例
    def logId(self):
        print(self.id)

