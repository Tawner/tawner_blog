from flask import Flask
from flask_cors import CORS
from config.settings import config
from flask_script import Manager
from flask_migrate import MigrateCommand
from common.system.middleware import middleware_register
from common.system.errors import error_handler


def register_blueprints(app):
    """蓝图注册"""
    from .v1 import blue_print
    app.register_blueprint(blue_print(), url_prefix='/api/v1.0')


def register_plugin(app):
    """插件注册"""
    from common.models.base import db
    from flask_migrate import Migrate
    from common.marshmallow import marshmallow
    from common.email import mail
    # 邮箱
    mail.init_app(app)
    # 数据格式化
    marshmallow.init_app(app)
    # 数据库
    db.init_app(app)
    # 版本管理
    migrate = Migrate(app, db)
    # 命令行
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    return manager


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 跨域
    CORS(app)
    # 注册蓝图
    register_blueprints(app)
    # 注册插件
    manager = register_plugin(app)
    # 注册中间件
    middleware_register(app)
    # 统一异常
    error_handler(app)
    return app, manager



