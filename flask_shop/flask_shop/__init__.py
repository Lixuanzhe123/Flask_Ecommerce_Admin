from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config_map

db=SQLAlchemy()
def create_app(config_name):


    app=Flask(__name__)
    
    # 解决中文乱码
    app.json.ensure_ascii = False

    config=config_map.get(config_name)
    # 配置
    app.config.from_object(config)

    # 数据库
    db.init_app(app)

    from flask_shop.user import user_bp
    from flask_shop.menu import menu_bp
    from flask_shop.roles import role_bp
    from flask_shop.group import cg_bp,attr_bp
    from flask_shop.product import pro_bp
    from flask_shop.order import ord_bp

    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(cg_bp)
    app.register_blueprint(attr_bp)
    app.register_blueprint(pro_bp)
    app.register_blueprint(ord_bp)
    return app
