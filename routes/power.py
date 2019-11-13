from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
import time, json
from utils import log
from models.user import User, db
from models.seat import Seat

main = Blueprint('power', __name__)

# 加载功能列表页面
@main.route('/power', methods=['POST', 'GET'])
def power():
    return render_template('power_list.html')