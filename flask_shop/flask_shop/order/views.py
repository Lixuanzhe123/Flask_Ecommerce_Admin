from flask_restful import Resource,reqparse

from flask_shop.order import ord_bp,ord_api
from flask_shop import db
from flask_shop import models

class Orders(Resource):
    #获取订单
    def get(self):
        try:
            parse=reqparse.RequestParser()

            parse.add_argument("name",type=str,location="args")

            #解析函数
            args=parse.parse_args()

            if args.get("name"):
                orders=models.Order.query.filter(models.Order.name.like(f'{args.get("name")}')).all()

            else:
                orders=models.Order.query.all()
            order_list=[order.to_dict() for order in orders]
            return {"status":200,"msg":"获取成功","data":order_list}
        except Exception as e:
            print(e)
            return {"status":400,"msg":"获取订单失败"}

ord_api.add_resource(Orders,"/orders/")

class Order(Resource):
    '''
        获取单个订单
    '''
    def get(self,id):
        try:
            order=models.Order.get(id)

            return {"status":200,"msg":"获取成功","data":order.to_dict()}
        except Exception as e:
            return {"status":400,"msg":"获取失败"}

ord_api.add_resource(Order,"/order/<int:id>")

class Express(Resource):
    '''
        获取订单物流信息
    '''
    def get(self,id):
        try:
            express_list=models.Express.query.filter(models.Express.oid==id).order_by(models.Express.update_time.desc()).all()
            return {"status":200,"msg":"获取信息成功","data":[express.to_dict() for express in express_list]}
        except Exception as e:
            return {"status":400,"msg":"获取信息失败"}

ord_api.add_resource(Express,"/express/<int:id>/")