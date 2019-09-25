from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    session,
    url_for,
)
from models.client import db, Client
import time, json
from utils import log, serialize
main = Blueprint('client', __name__)


# 加载客户页面
@main.route('/client', methods=['POST', 'GET'])
def client_page():
    content = {}
    infos =[]
    cliets = Client.query.all()
    for c in cliets:  # c是model对象，使用.取就行
        log('取到的客户记录', c.id, c.cid, c.number, c.name, c.qq, c.wechat, c.email)
        client = dict(
            id = c.id,
            name = c.name,
            phone = c.number,
            company = c.cid,
            wechat = c.wechat,
            qq = c.qq,
            email = c.email,
        )
        infos.append(client)
    content['c_info'] = infos
    log(content)
    return render_template('client.html', **content)


# 给ajax发送请求的数据。取消按钮，发送json数据
@main.route('/load_clients', methods=['POST'])
def load_clients():
    log('改动客户信息就重新加载所有客户的信息...')
    cs = []
    cliets = Client.query.all()
    for c in cliets:  # c是model对象，使用.取就行
        log('取到的客户记录', c.id, c.cid, c.number, c.name, c.qq, c.wechat, c.email)
        client = dict(
            id = c.id,
            name = c.name,
            phone = c.number,
            company = c.cid,
            wechat = c.wechat,
            qq = c.qq,
            email = c.email,
        )
        cs.append(client)
    # 将其转换成json的字符串
    json_cs = json.dumps(cs)
    # log('后台发送的json格式的字符串', json_cs)
    return json_cs


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


# 前端ajax搜索客户,模糊查询, model对象转成dict对象, or_的使用
@main.route('/find_client', methods=['POST'])
def find_client():
    from sqlalchemy import or_
    name = request.form.get('data')
    all_results = Client.query.filter(or_(
        Client.name.like("%" + name + "%") ,
        Client.number.like("%" + name + "%"),
        Client.qq.like("%" + name + "%"),
    )).all()
    # all_results = Client.query.filter(Client.number.like('%'+name+'%')).all()
    log(all_results)
    all_r_dict = serialize(all_results)
    log('序列化的结果', all_r_dict)
    all_r_json = jsonify(all_r_dict)
    log('传输给前端的东西', all_r_json)
    return all_r_json

# 前端增加
@main.route('/add_client', methods=['POST'])
def add_client():
    new_client = request.form
    id = new_client.get('cid')
    name = new_client.get('name')
    cid = new_client.get('gs')
    number = new_client.get('phone')
    wechat = new_client.get('wechat')
    qq = new_client.get('qq')
    email = new_client.get('email')
    c = Client(id=id, cid=cid,
                       number=number, name=name, wechat=wechat, email=email, qq=qq)
    db.session.add(c)
    db.session.commit()
    return 'add sucess'
