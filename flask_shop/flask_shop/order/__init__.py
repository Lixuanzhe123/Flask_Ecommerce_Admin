from flask import Blueprint
from flask_restful import Api

ord_bp=Blueprint("order",__name__)
ord_api=Api(ord_bp)

from . import views