from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
)
from functools import wraps

main = Blueprint('index', __name__)

# 通话记录
@main.route('/call_record')
def call_record():
    return render_template('callRecord.html')


# 录音记录
@main.route('/voice_record')
def voice_record():
    return render_template('voiceRecord.html')
