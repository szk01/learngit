from . import db


# 客户公司表
class Ccompany1(db.Model):
    __tablename__ = 'ccompany1'

    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer)
    c_code = db.Column(db.String(20))
    name = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(255))
    industry = db.Column(db.String(255))
    route_range = db.Column(db.String(255))
    principal_name = db.Column(db.String(15))

# 公司客户表
# class Ccompany(db.Model):
#     __tablename__ = 'ccompany'
#
#     id = db.Column(db.Integer, primary_key=True)
#     c_code = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                             # 公司代码
#     name = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False)              # 公司名
#     phone = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))                             # 公司电话
#     email = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                              # 公司邮箱
#     area = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))                              # 公司地址
#     main_class = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                         # 主分类： 普通客户
#     type = db.Column(db.String(255))                                                    #
#     banker = db.Column(db.String(50, 'utf8mb4_es_0900_ai_ci'))                          # 庄家（给出货运价格的角色）
#     industry = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                           # 行业 （如运输行业）
#     route_range = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                        # 航线范围
#     client_source = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                      # 客户来源（平台， 网站）
#     platform = db.Column(db.String(50))
#     address = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))                           # 地址（广东深圳罗湖区）
#     ct = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     ut = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     client_code = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                        # 客户代码
#     qq = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
#     main_route = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                         # 主打行业
#     url = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                                # 网址
#     department = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))                         # 所属部门
#     contact_name = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                       # 联系人姓名
#     contact_sex = db.Column(db.String(2, 'utf8mb4_0900_ai_ci'))                         # 联系人性别
#     contact_unit_phone = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                 # 联系人——单位电话
#     contact_fax = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                        # 联系人传真
#     contact_phone = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                      # 联系人手机
#     contact_msn = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                        # 联系人msn
#     contact_c_email = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                    # 联系人公司邮件
#     contact_p_email = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                    # 联系人私人邮件
#     contact_add = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))                       # 联系人通讯地址
#     contact_postal_code = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                # 联系人邮政编码
#     contact_role = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                       # 联系人角色
#     contact_qq = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))                         # 联系人qq