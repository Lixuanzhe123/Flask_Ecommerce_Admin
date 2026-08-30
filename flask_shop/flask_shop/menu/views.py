from flask_shop.menu import menu_api
from flask_restful import Resource
from flask import request


from flask_shop.models import Menu


class Menus(Resource):
    # 获取一级菜单
    def get(self):
        type_=request.args.get('type_')
        if type_=='trea':
            menus=Menu.query.filter(Menu.level==1).all()
            menus_list=[]
            for menu in menus:
                menus_list.append(menu.to_dict_trea())

            return {'code':200,'msg':'获取成功','data':menus_list}
        else:
            menus=Menu.query.filter(Menu.level!=0).all()
            menus_list=[menu.to_dict() for menu in menus]

            return {'code':200,'msg':'获取成功','data':menus_list}
    
    

menu_api.add_resource(Menus,'/menus/')