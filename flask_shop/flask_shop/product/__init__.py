from flask import Blueprint
from flask_restful import Api

pro_bp=Blueprint("product",__name__)
pro_api=Api(pro_bp)


from . import views