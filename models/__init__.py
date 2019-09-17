from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker

# 创建数据库操作对象
db = SQLAlchemy()
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/nonghao')          # 这个是用来与mysql数据库交互的
# DBSession = sessionmaker(bind=engine)
# session = DBSession()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
