
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 创建数据库操作对象
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
