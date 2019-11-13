from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)

from models.ccompany import Ccompany1, db
from utils import log

main = Blueprint('ccompany', __name__)

# 分页
@main.route('/ccompany', methods=['GET', 'POST'])
def new_client():
    content = {}
    current_page = request.args.get('page', 1, type=int)  # 从查询字符串获取当前页数
    pagination = Ccompany1.query.paginate(current_page, per_page=10)
    ccomps = pagination.items                          # items当前页面中的记录
    content['pagination'] = pagination
    content['ccomps'] = ccomps

    return render_template('ccompany.html', **content)


# ajax 删除客户公司，未做权限验证
@main.route('/delete/com_user', methods=['POST'])
def delete_company():
    cid = request.form.get('com_id')
    # 找到对应的客户公司，然后删除它
    log('id', cid)
    com = Ccompany1.query.filter_by(id=int(cid)).first()
    db.session.delete(com)
    db.session.commit()
    log('删除客户成功')
    return 'delete success'


# ajax 编辑公司信息
@main.route('/update/company', methods=['POST'])
def update_company():
    form = request.form
    log('form', form)
    id = form.get("c_id")
    name = form.get("c_name")
    phone = form.get("c_phone")
    address = form.get("c_address")
    industry = form.get("c_industry")
    range = form.get("c_range")

    ccom = Ccompany1.query.get(int(id))
    ccom.name = name
    ccom.phone = phone
    ccom.address = address
    ccom.industry = industry
    ccom.range = range
    db.session.commit()
    return 'update success'

# ajax 新增一家公司
@main.route('/new/company', methods=['POST'])
def new_company():
    form = request.form
    log('form', form)

    name = form.get("name")
    phone = form.get("phone")
    address = form.get("address")
    route_range = form.get("route_range")
    industry = form.get("industry")
    com = Ccompany1(name=name, phone=phone, address=address, route_range=route_range, industry=industry)
    db.session.add(com)
    db.session.commit()
    return "new success"

