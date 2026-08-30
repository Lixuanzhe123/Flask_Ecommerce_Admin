from flask_restful import Resource,reqparse
import hashlib
from time import time


from flask import current_app, request
from flask_shop.group import cg_api,attr_api,attr_bp,cg_bp
from flask_shop.models import Category,Attribute
from flask_shop import db


class Gategorys(Resource):
    def get(self):
        try:
            pnum=request.args.get('pnum')
            psize=request.args.get('psize')
            level=request.args.get('level')
           
            level=int(level)
            if not level:
                level=3
            base_cates=Category.query.filter(Category.level==1)
            if all([pnum,psize]):
                cates=base_cates.paginate(page=pnum,per_page=psize)
            else:
                cates=base_cates.all()
            cates_list=self.to_dict(info=cates,level=level)
            return {'code':200,'message':'获取分类列表成功','data':cates_list}
        except Exception as e:
            print(e)
            return {'code':400,'message':'服务器错误'}
        
    def to_dict(self,info:list,level:int):
        c_list=[]

        for c in info:
            c_dict=c.to_dict()
            if c.level<level:
                c_dict['children']=self.to_dict(info=c.children,level=level)
            c_list.append(c_dict)
        return c_list


    def post(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('name',type=str,required=True,help='请输入分类名称')
            parser.add_argument('level',type=int,required=True,help='请输入分类级别')
            parser.add_argument('pid',type=int,required=False,help='请输入父级分类id')

            arg=parser.parse_args()

            if arg.get('pid'):
                c=Category(name=arg.get('name'),level=arg.get('level'),pid=arg.get('pid'))

            else:
                c=Category(name=arg.get('name'),level=arg.get('level'))
            db.session.add(c)
            db.session.commit()
            return {'code':200,'msg':'添加分类成功','data':c.to_dict()}
        except Exception as e:
            print(e)
            return {'code':400,'msg':'服务器错误'}
            

cg_api.add_resource(Gategorys,'/')

class category(Resource):
    def get(self,id):
        '''
        搜查该商品，以及其子商品
        '''
        try:
            c=Category.query.get(id)
            c_list=self.to_dict(info=c)
            return {"status":200,"data":c_list}
            
        except Exception as e:
            print(e)
            return {"status":400,"msg":"获取失败"}

    def to_dict(self,info:list):
        c_list=[]
        if c.children
        for c in info:
            c_dict=c.to_dict()
            if c.children:
                c_dict["chilren"]=self.to_dict(info=c.children)
            c_list.append(c_dict)
        return c_list
        
                

    def delete(self,id):
        pass
cg_api.add_resource(category,'/<int:id>/')


# 属性接口
class AttriButes(Resource):
    def get(self):
        try:
            # 参数
            parms=reqparse.RequestParser()
            parms.add_argument('cid',type=int,required=True,help='请输入分类id',location='args')
            parms.add_argument('_type',type=str,required=True,help='请输入属性类型',location='args')

            # 解析参数
            args=parms.parse_args()

            atts=Attribute.query.filter(Attribute.cid==args.get('cid')).all()

            atts_list=[]

            if args.get('_type')=='static':
                atts_list=[att.to_dict() for att in atts if att._type=='static']
            else:
                atts_list=[att.to_dict() for att in atts if att._type=='dynamic']
            return {'code':200,'msg':'获取属性列表成功','data':atts_list}

        except Exception as e:
            print(e)
            return {'code':400,'msg':'服务器错误'}
        
    def post(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('name',type=str,required=True,help='请输入属性名称')
            parser.add_argument('val',type=str,help='请输入属性值')
            parser.add_argument('cid',type=int,required=True,help='请输入分类id')
            parser.add_argument('_type',type=str,required=True,help='请输入属性类型')

            args=parser.parse_args()

            if args.get('val'):
                att=Attribute(name=args.get('name'),val=args.get('val'),cid=args.get('cid'),_type=args.get('_type'))
            else:
                att=Attribute(name=args.get('name'),cid=args.get('cid'),_type=args.get('_type'))
            db.session.add(att)
            db.session.commit()
            return {'code':200,'msg':'添加属性成功','data':att.to_dict()}
        except Exception as e:
            print(e)
            return {'code':400,'msg':'服务器错误'}


class AttriBute(Resource):
    # 获取某个属性
    def get(self,id:int):
        try:
            att=Attribute.query.get(id)
            if att:
                return {'code':200,'msg':'获取属性成功','data':att.to_dict()}
            else:
                return {'code':400,'msg':'属性不存在'}
        except Exception as e:
            print(e)
            return {'code':400,'msg':'服务器错误'}
    # 修改某个属性
    def put(self,id:int):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('name',type=str,help='请输入属性名称')
            parser.add_argument('val',type=str,help='请输入属性值')
            parser.add_argument('cid',type=int,help='请输入分类id')
            parser.add_argument('_type',type=str,help='请输入属性类型')

            args=parser.parse_args()
            att=Attribute.query.get(id)

            if not att:
                return {'code':400,'msg':'属性不存在'}

            if args.get('name'):
                att.name=args.get('name')
            if args.get('val'):
                att.val=args.get('val')
            if args.get('cid'):
                att.cid=args.get('cid')
            if args.get('_type'):
                att._type=args.get('_type')
            db.session.commit()
            return {'code':200,'msg':'修改属性成功','data':att.to_dict()}
        except Exception as e:
            print(e)
            return {'code':400,'msg':'服务器错误'}
    # 删除某个属性
    def delete(self,id:int):
        try:
            att=Attribute.query.get(id)
            if att:
                db.session.delete(att)
                db.session.commit()
                return {'code':200,'msg':'删除属性成功'}
            else:
                return {'code':400,'msg':'属性不存在'}
        except Exception as e:
            print(e)
            return {'code':400,'msg':'服务器错误'}

attr_api.add_resource(AttriButes,'/attributes/')
attr_api.add_resource(AttriBute,'/attribute/<int:id>/')

@attr_bp.route('/upload_img',methods=['POST'])
def upload_img():
    img_file=request.files.get('file')

    # 检查图片是否为空
    if not img_file:
        return {'code':500,'msg':'请上传图片'}

    #检查图片是否是允许上传的类型
    if allowed_img(img_file.filename):
        #保存图片
        
        #获得储存文件
        floder=current_app.config['UPLOAD_FOLDER']
        #生成随机文件名
        file_name=md5_file()+'.'+img_file.filename.rsplit('.',1)[1]
        #保存图片
        img_file.save(f"{floder}/{file_name}")

        data={
            'path':f"/static/upload/{file_name}",
            'url':f'http://127.0.0.1:5000/static/upload/{file_name}'
        }
        return {'code':200,'msg':'上传图片成功','data':data}
    else:
        return {'code':500,'msg':'图片类型不允许上传'}

def allowed_img(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in current_app.config['ALLOWED_EXTENSIONS']
    
def md5_file():
    '''
    生成随机文件名
    '''
    #创建hashlib对象
    md5=hashlib.md5()

    #获得当前的时间戳
    timestamp=str(time())

    #将时间戳进行加密
    md5.update(timestamp.encode())

    #获得加密后的字符
    file_name=md5.hexdigest()
    return file_name

from sqlalchemy import func,text

@cg_bp.route("/cate_group/")
def cate_groud():
    '''
        分类列表的等级水平统计
    '''
    try:
        #用方法一分组
        # rs=db.session.query(Category.level,func.count(1)).group_by(Category.level).all()
        #当复杂时，直接用sql语句快点
        sql="select t_category.level,count(1) from t_category group by level"
        rs=db.session.execute(text(sql)).all()
        data={
            "name":"分类数量",
            "xAxis":[f"{r[0]}级分类" for r in rs],
            "series":[r[1] for r in rs]
        }
        return {"status":200,"msg":"获取数据成功","data":data}
    except Exception as e:
        return {"status":400,"msg":"服务器错误"}