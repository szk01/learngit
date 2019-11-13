'''
初始化app实例
注册socketio拓展
连接数据库db
'''

from flask import Flask
from flask_socketio import SocketIO
from models import db
from models import config

from routes.index import main as index_routes
from routes.login import main as login_routes
from routes.test import main as test_routes
from routes.client import main as client_routes
from routes.account import main as account_routes

socketio = SocketIO()


def create_app():

    app = Flask('flask20')
    app.secret_key = 'secret_key'
    socketio.init_app(app)          # 注册拓展socketio

    app.config.from_object(config)
    print('config', app.config)
    db.init_app(app)

    register_blueprints(app)        # 注册蓝图
    return app


# 注册蓝图
def register_blueprints(app):
    app.register_blueprint(index_routes, url_prefix='')
    app.register_blueprint(test_routes, url_prefix='')
    app.register_blueprint(login_routes, url_prefix='')
    app.register_blueprint(client_routes, url_prefix='')
    app.register_blueprint(account_routes, url_prefix='')
