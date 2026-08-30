from flask import Blueprint
from flask_restful import Api

# 创建蓝图
user_bp=Blueprint('user',__name__,url_prefix='/user')

api=Api(user_bp)


from . import views

