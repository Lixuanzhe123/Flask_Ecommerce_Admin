from flask import Blueprint
from flask_restful import Api

#商品分类蓝图
cg_bp=Blueprint('cg',__name__,url_prefix="/category")
#商品属性蓝图
attr_bp=Blueprint('attr',__name__)

#商品分类接口
cg_api=Api(cg_bp)
#商品属性接口
attr_api=Api(attr_bp)

from . import views