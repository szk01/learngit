from . import db


class Company(db.Model):
    # 公司表
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    c_code = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'))                                 # 公司代码
    name = db.Column(db.String(255), nullable=False)                                        # 公司名称
    principal_name = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'), nullable=False)         # 公司负责人
    p_uid = db.Column(db.Integer)                                                           # 负责人账号ID
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
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())            # 状态0正常1停用2过期
    cid = db.Column(db.ForeignKey('company.id'), nullable=False, index=True)                    # 外键关联到公司表 所属公司ID
    permit = db.Column(db.String(255))                                                          # 功能权限
    create_time = db.Column(db.BigInteger, nullable=False)
    update_time = db.Column(db.BigInteger)
    over_time = db.Column(db.BigInteger, nullable=False)

    company = db.relationship('Company', primaryjoin='CompanyPermit.cid == Company.id', backref='company_permits')
