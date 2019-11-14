from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    session,
    url_for,
)
from models.client import db, Client1
from models.ccompany import Ccompany1
import time, json
from utils import log, serialize
main = Blueprint('client', __name__)


# 加载客户页面
@main.route('/client', methods=['POST', 'GET'])
def client_page():
    content = {}
    current_page = request.args.get('page', 1, type=int)  # 从查询字符串获取当前页数
    pagination = Client1.query.paginate(current_page, per_page=10)
    clients = pagination.items                          # items当前页面中的记录
    content['pagination'] = pagination
    content['clients'] = clients

    return render_template('client.html', **content)


# ajax删除客户
@main.route('/delete/client', methods=['POST'])
def delete_client():
    id = request.form.get("id")
    log('id', type(id), id)
    client1 = Client1.query.filter_by(id=int(id)).first()
    db.session.delete(client1)
    db.session.commit()
    return "delete success"


def find_com(company):
    com1 = Ccompany1.query.filter_by(name=company).first()
    log('company', company)
    if com1:                            # 如果存在
        id = com1.id
        return id

# ajax增加客户
@main.route('/new/client', methods=['POST'])
def new_client():
    form = request.form
    log('form', form)
    name = form.get("name")
    sex = form.get("sex")
    phone = form.get("phone")
    position = form.get("position")
    qq = form.get("qq")

    company = form.get("company")
    com = find_com(company)
    log('id', com)
    # 如果公司存在，找出所在的id,填写其com_id
    if isinstance(com, int):
        c = Client1(name=name, com_id=com, sex=sex, phone=phone, position=position, qq=qq)
        db.session.add(c)
        db.session.commit()
        log('增加客户成功')
    return "new success"


# ajax查找公司， 模糊查询，只要前10个
@main.route('/find/companys', methods=['POST'])
def find_companys():

    data = request.form.get("data")
    log("data", data)
    coms = Ccompany1.query.with_entities(Ccompany1.id, Ccompany1.name).filter(
            Ccompany1.name.like('%'+data + "%") if data is not None else ""

        ).limit(10).all()

    n = len(coms)

    if n == 0:
        companys = []
        for c in coms:
            log('name', c)
            companys.append(c.name)
        return jsonify(companys)
    else:
        return ''


# ajax，搜索请求

# 前端页面发送ajax请求，保存信息，修改数据库中的记录
@main.route('/client_update', methods=['POST'])
def client_save():
    client_info = request.form
    id = client_info.get('c_cid')
    log('前端页面传过来的信息', id)
    client = Client.query.get(id)
    log('更新信息', client)
    client.name = client_info.get('c_name')
    client.number = client_info.get('c_phones')
    client.cid = client_info.get('c_gs')
    client.qq = client_info.get('c_wechats')
    client.wechat = client_info.get('c_qqs')
    client.email = client_info.get('c_mails')
    db.session.commit()
    return 'edit sucess'

# 前端ajax搜索公司,模糊查询, model对象转成dict对象, or_的使用
@main.route('/find_client', methods=['POST'])
def find_client():
    from sqlalchemy import or_
    name = request.form.get('data')
    all_results = Ccompany1.query.filter_by(
        Ccompany1.name.like("%" + name + "%")
    ).all()
    # all_results = Client.query.filter(Client.number.like('%'+name+'%')).all()
    log('all_companys', all_results)
    all_r_dict = serialize(all_results)
    log('序列化的结果', all_r_dict)
    all_r_json = jsonify(all_r_dict)
    log('传输给前端的东西', all_r_json)
    return all_r_json

# 增加一个客户
# @main.route('/add_client', methods=['POST'])
# def add_client():
#     new_client = request.form
#     # id = new_client.get('cid')
#     name = new_client.get('name')
#     cid = new_client.get('gs')                  # 公司
#     number = new_client.get('phone')
#     wechat = new_client.get('wechat')
#     qq = new_client.get('qq')
#     email = new_client.get('email')
#     c = Client(cid=cid, number=number, name=name, wechat=wechat, email=email, qq=qq)
#     db.session.add(c)
#     db.session.commit()
#     return 'add sucess'
