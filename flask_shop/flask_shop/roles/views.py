from flask_restful import Resource,reqparse
from flask import request

from flask_shop.roles  import role_api,role_bp
from flask_shop import models,db

class Roles(Resource):
    def get(self):
        try:
            roles=models.Role.query.all()
            role_list=[role.to_dict() for role in roles]
            return {'code':200,'message':'获取角色列表成功','data':role_list}
        except Exception as e:
            return {'code':400,'message':'获取角色列表失败'}
        
    def post(self):
        try:
            name=request.get_json().get('name')#content-type:application/json
            description=request.get_json().get('description')
            role=models.Role(name=name,description=description)
            db.session.add(role)
            db.session.commit()
            return {'code':200,'message':'添加角色成功','data':role.to_dict()}
        except Exception as e:
            print(e)
            return {'code':400,'message':'添加角色失败'}


        
role_api.add_resource(Roles,'/roles/')

class Role(Resource):
    #删除角色
    def delete(self,id):
        try:
            role=models.Role.query.get(id)
            if role:
                db.session.delete(role)
                db.session.commit()
                return {'code':200,'message':'删除角色成功'}
            return {'code':400,'message':'角色不存在'}
        except Exception as e:
            return{'code':400,'message':'删除角色失败'}
    
    #修改角色
    def put(self,id):
        try:
            params=reqparse.RequestParser()
            params.add_argument('name',type=str,required=True,help='角色名称不能为空')
            params.add_argument('description',type=str)
            args=params.parse_args()

            name=args.get('name')
            description=args.get('description')
            role=models.Role.query.get(id)
            if role:
                if name:
                    role.name=name
                if description:
                    role.description=description
                db.session.commit()
                return {'code':200,'message':'修改角色成功'}
            else:
                return {'code':400,'message':'角色不存在'}
        except Exception as e:
            return {'code':400,'message':'修改失败'}
        


 #删除角色菜单       
@role_bp.route('/roles/<int:r_id>/<int:m_id>/',methods=['DELETE'])
def delete_role_menu(r_id,m_id):
    try:
        role=models.Role.query.get(r_id)
        menu=models.Menu.query.get(m_id)
        if role and menu:
            if menu in role.menus:
                if menu.level==1:
                    for role_menu in role.menus:
                        if role_menu in menu.children:
                            role.menus.remove(role_menu)   
                else:
                    role.menus.remove(menu)
                db.session.commit()
                return {'code':200,'message':'删除成功'}
            return {'code':400,'message':'角色未关联此菜单'}
        return {'code':400,'message':'角色或菜单不存在'}
    except Exception as e:
        return {'code':400,'message':'删除失败'}


#分配权限
@role_bp.route('/<int:r_id>/',methods=['POST'])
def add_role_menu(r_id):
    try:
        role=models.Role.query.get(r_id)
        mids=request.get_json().get('mids')

        role.menus=[]
        mids=mids.split(',')
        for mid in mids:
            if mid:
                menu=models.Menu.query.get(mid)
                role.menus.append(menu)
        db.session.commit()
        return {'code':200,'message':'分配成功'}
    except Exception as e:
        return {'code':400,'message':'分配失败'}

role_api.add_resource(Role,'/role/<int:id>/')
            