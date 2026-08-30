from flask_restful import reqparse,Resource

from flask_shop.product import pro_api
from flask_shop import db
from flask_shop.models import Product,Picture,ProductAttr

class Products(Resource):
    def get(self):
        try:
        #解析
            parms=reqparse.RequestParser()

            parms.add_argument("name",type=str,location="args")

            args=parms.parse_args()

            name=args.get("name")

            if name:
                p_list=Product.query.filter(Product.name.like(f"%{name}%")).all()
        
            else:
                p_list=Product.query.all()
            return {
                "status":200,
                "msg":"获取商品列表成功",
                'data':[product.to_dict() for product in p_list]
            }
        except Exception as e:
            print(e)
            return {"status":400,"msg":"服务器错误"}
    def post(self):
        try:
            parms=reqparse.RequestParser()

            parms.add_argument("name",type=str,required=True,help="商品名称不能为空")
            parms.add_argument("price",type=float,required=True,help='商品价格不能为空')
            parms.add_argument("number",type=int)
            parms.add_argument("introduce",type=str)
            parms.add_argument("weight",type=int)
            parms.add_argument('cid_one',type=int)
            parms.add_argument('cid_two',type=int)
            parms.add_argument('cid_three',type=int)

            parms.add_argument("pics",type=list,location='json')
            parms.add_argument("attr_static",type=list,location='json')
            parms.add_argument("attr_dynamic",type=list,location="json")

            args=parms.parse_args()

            #给Prouduct赋值
            Pro=Product(
                name=args.get('name'),
                price=args.get('price'),
                number=args.get('number'),
                introduce=args.get('introduce'),
                weight=args.get('weight'),
                cid_one=args.get('cid_one'),
                cid_two=args.get('cid_two'),
                cid_three=args.get('cid_three')
            )

            db.session.add(Pro)
            db.session.commit()

            #picture赋值
            for p in args.get('pics'):
                pic=Picture(
                    pid=Pro.id,
                    path=p
                )
                db.session.add(pic)
            
            #ProductAttrdong静态赋值
            for p_a in args.get('attr_static'):
                Pa=ProductAttr(
                    pid=Pro.id,
                    aid=p_a.get("id"),
                    val=p_a.get("val"),
                    _type="static"
                )
                db.session.add(Pa)
            
            #ProductAttrdong静态赋值
            for p_a in args.get("attr_dynamic"):
                Pa=ProductAttr(
                    pid=Pro.id,
                    aid=p_a.get("id"),
                    val=",".join(p_a.get("val")),
                    _type="dynamic"
                )
                db.session.add(Pa)
            db.session.commit()
            return {"status":200,"msg":"添加成功"}
        except Exception as e:
           print(e)
           return {"status":400,"msg":"添加失败"}


pro_api.add_resource(Products,"/products/")

class product(Resource):
    def delete(self,id):
        try:
            pro=Product.query.get(id)
            db.session.delete(pro)
            db.session.commit()
            return {"status":200,"msg":"删除商品成功"}
        except Exception as e:
            return {"status":500,"msg":"删除商品失败"}
        

pro_api.add_resource(product,"/product/<int:id>/")
