from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
)
from functools import wraps

main = Blueprint('index', __name__)


def login_required(func):
    @wraps(func)
    def qingwa(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return qingwa


@main.route('/index', methods=['GET'])
@login_required
def index():
    if current_user.is_active:
        return render_template('index.html')
    else:
        return redirect('/login')
    return '成功'

# 通话记录
@main.route('/call_record')
def record():
    return render_template('callRecord.html')


# 录音记录
@main.route('/voice_record')
def record():
    return render_template('voiceRecord.html')
