from flask import request
from flask_restful import Resource,reqparse
import re

from flask_shop.user import user_bp,api
from flask_shop import models,db
from flask_shop.utils import token
@user_bp.route('/')
def index():
    return 'user index'


@user_bp.route('/login/',methods=['POST'])
def login():
    # 获取用户名
    # uname=request.form.get('username') # content-type:application/x-www-form-urlencoded
    uname=request.get_json().get('username') #content-type:application/json
    password=request.get_json().get('pwd')

    if not all([uname,password]):
        return {'code':400,'msg':'用户名或密码不能为空'}


    user=models.User.query.filter(models.User.username==uname).first()

    if user and user.check_password(password):
        # 生成token
        token1=token.generate_token({'id':user.id})
        return {'code':200,'msg':'登录成功','data':{'token':token1}}
    else:
        return {'code':400,'msg':'用户名或密码错误'}

class Users(Resource):
    def get(self):
        #创建RequestParser对象
        parser=reqparse.RequestParser()
        # 添加参数
        parser.add_argument('pnum',type=int,default=1,location='args')
        parser.add_argument('psize',type=int,default=3,location='args')
        parser.add_argument('name',type=str,location='args')


        #解析参数
        args=parser.parse_args()
        # 获取参数
        name=args.get('name')
        pnum=args.get('pnum')
        psize=args.get('psize')
        #判断是否转递name
        if name:
            user_list=models.User.query.filter(models.User.username.like(f'%{name}%')).paginate(page=pnum,per_page=psize)
        else:
            # 获取所有用户
            user_list=models.User.query.paginate(page=pnum,per_page=psize)
        data={
            'total':user_list.total,
            'pnum':pnum,
            'data':[user.to_dict() for user in user_list.items]
        }
        return {'code':200,'msg':'获取用户列表成功','data':data}

    

    def post(self):
   
        uname=request.get_json().get('name') #content-type:application/json
        pwd=request.get_json().get('password')
        re_pwd=request.get_json().get('re_password')
        email=request.get_json().get('email')
        phone=request.get_json().get('phone')
        nick_name=request.get_json().get('nick_name')
        role_id=request.get_json().get('role_id')


        if not all([uname,pwd,email]):
            return {'code':400,'msg':'用户名或密码不能为空'}
        #密码中含有6-20个字符，且有数字、字母
        if not re.match(r'^(?=.*[0-9])(?=.*[a-zA-Z]).{6,20}$',pwd):
            return {'code':400,'msg':'密码中含有6-20个字符,且有数字、字母'}
        if re_pwd!=pwd:
            return {'code':400,'msg':'两次密码不一致'}
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email):
            return {'code':400,'msg':'邮箱格式错误'}
        if not re.match(r'^1[3-9]\d{9}$',phone):
            return {'code':400,'msg':'手机号格式错误'}
        if (len(uname)<=5 or len(uname)>20):
            return {'code':400,'msg':'用户名长度必须在5-20之间'}
        
        try:
            user= models.User.query.filter(models.User.username==uname).first()
            if user:
                return {'code':400,'msg':'用户名已存在'}
            user= models.User.query.filter(models.User.email==email).first()
            if user:
                return {'code':400,'msg':'邮箱已存在'}
            user= models.User.query.filter(models.User.phone==phone).first()
            if user:
                return {'code':400,'msg':'手机号已存在'}
            user= models.User.query.filter(models.User.nick_name==nick_name).first()
            if user:
                return {'code':400,'msg':'昵称已存在'}
        except Exception as e:
            return {'code':400,'msg':'服务器错误'}
        
        if role_id==None:
            role_id=1
        try:
            user= models.User(username=uname,password=pwd,email=email,phone=phone,nick_name=nick_name,role_id=role_id)
            db.session.add(user)
            db.session.commit()
            return {'code':200,'msg':'注册成功'}
        except Exception as e:
            # print(e)
            return {'code':400,'msg':'服务器错误'}

class User(Resource):
    def get(self,id):
        user=models.User.query.get(id)

        if user:
            return {'code':200,'msg':'获取用户信息成功','data':user.to_dict()}
        else:
            return {'code':400,'msg':'用户不存在'}

    def put(self,id):
        try:
            user=models.User.query.get(id)
            #创建ReuestParser对象,用来接收数据
            paser=reqparse.RequestParser()
            paser.add_argument('nick_name',type=str)
            paser.add_argument('phone',type=str)
            paser.add_argument('email',type=str)
            paser.add_argument('username',type=str)
            paser.add_argument('role_id',type=int)

            # 解析参数
            args=paser.parse_args()
            if args.get('nick_name'):
                user.nick_name=args.get('nick_name')
            if args.get('phone'):
                user.phone=args.get('phone')
            if args.get('email'):
                user.email=args.get('email')
            if args.get('username'):
                user.username=args.get('username')
            if args.get('role_id'):
                user.role_id=args.get('role_id')
            db.session.commit()
            return {'code':200,'msg':'修改用户信息成功','data':user.to_dict()}
        except Exception as e:
            print(e)
            
            return {'code':400,'msg':'服务器错误'}


    def delete(self,id):
        try:
            user=models.User.query.get(id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return {'code':200,'msg':'删除用户成功'}
        except Exception as e:
                print(e)
                return {'code':400,'msg':'用户不存在'}



@user_bp.route('/reset_password/<int:id>/',methods=['Put'])
# @token.login_required
def reset_password(id):
    try:
        parser=reqparse.RequestParser()
        parser.add_argument('password',type=str)

        args=parser.parse_args()
        password=args.get('password')
        user=models.User.query.get(id)
        if user:
            user.password=password
            db.session.commit()
            return {'code':200,'msg':f'密码重置成功,密码为:{password}'}
        else:
            return {'code':400,'msg':'用户不存在'}
    except Exception as e:
        return {'code':400,'msg':'密码重置失败1'}




@user_bp.route('/test/',methods=['GET'])
@token.login_required
def index_info():
    return {'code':200,'msg':'token验证成功'}

api.add_resource(Users,'/users/')
api.add_resource(User,'/user/<int:id>/')