from flask import Blueprint
from flask_restful import Api


role_bp=Blueprint('role',__name__,url_prefix='/role')

role_api=Api(role_bp)   

from . import views