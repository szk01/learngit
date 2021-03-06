# encoding: utf-8

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import app
from models.user import db

manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# 根据mysql数据库中的表生成orm代码，把这两行代码放到命令行中执行
# pip install flask-sqlacodegen
# flask-sqlacodegen mysql+pymysql://root:123456@localhost:3306/nonghao --outfile model3.py --flask

