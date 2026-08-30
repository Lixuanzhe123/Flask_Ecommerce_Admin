from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

from flask_shop import db


class BaseModel(object):
   created_at=db.Column(db.DateTime,default=datetime.now)
   updated_at=db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

#用户
class User(BaseModel,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,nullable=False)
    pwd=db.Column(db.String(255),nullable=False)
    nick_name=db.Column(db.String(64),unique=True,nullable=False)
    email=db.Column(db.String(64),unique=True,nullable=False)
    phone=db.Column(db.String(64),unique=True,nullable=False)
    __tablename__='t_user'

    #多对一

    role_id=db.Column(db.Integer,db.ForeignKey('t_role.id'),nullable=True)


    @property
    def password(self):
        return self.pwd
    
    @password.setter
    def password(self,pwd):
        self.pwd=generate_password_hash(pwd)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    def to_dict(self):
        return {
            'id':self.id,
            'username':self.username,
            'nick_name':self.nick_name,
            'email':self.email,
            'phone':self.phone,
            'role':self.role.name if self.role else "",
            'role_id':self.role_id if self.role else "",
        }
    
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

trm=db.Table(
    "t_role_menu",
    db.Column('role_id',db.Integer,db.ForeignKey('t_role.id'),primary_key=True),
    db.Column('menu_id',db.Integer,db.ForeignKey('t_menu.id'),primary_key=True),
    
    mysql_charset='utf8mb4',
    mysql_engine='InnoDB'
    )

#菜单
class Menu(db.Model):
    __tablename__='t_menu'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True,nullable=False)
    level=db.Column(db.Integer)
    path=db.Column(db.String(64),unique=True,nullable=True)

    pid=db.Column(db.Integer,db.ForeignKey('t_menu.id'),default=1)
    children=db.relationship('Menu')

    roles=db.relationship('Role',secondary=trm,backref='menus')



    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    


    def to_dict_trea(self):
        return {
            'id':self.id,
            'name':self.name,
            'level':self.level,
            'path':self.path,
            'pid':self.pid,
            'children':[child.to_dict_trea() for child in self.children]
        }
    
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'level':self.level,
            'path':self.path,
            'pid':self.pid,
        }

#角色
class Role(db.Model):
    __tablename__='t_role'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(64),unique=True,nullable=False)
    description=db.Column(db.String(128),unique=True,nullable=True)

    #一对多
    users=db.relationship('User',backref='role')

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'desc':self.description,
            # 'menus':[menu.to_dict_trea() for menu in self.menus if menu.level==1]
            'menus':self.get_menu_list()
        }
    
    def get_menu_list(self):
        menu_list=[]
        menus=sorted(self.menus,key=lambda temp:temp.id)
        for menu in self.menus:
            if menu.level==1:
                first_menu=menu.to_dict()
                first_menu['children']=[]
                for m2 in self.menus:
                    if m2.level==2 and m2.pid==menu.id:
                        first_menu['children'].append(m2.to_dict())
                menu_list.append(first_menu)
        return menu_list


    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

#商品分类
class Category(db.Model):
    __tablename__='t_category'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(64),unique=True,nullable=False)
    level=db.Column(db.Integer)
    pid=db.Column(db.Integer,db.ForeignKey('t_category.id'),default=1)

    children=db.relationship('Category')

    attrs=db.relationship('Attribute',backref='category')

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'level':self.level,
            'pid':self.pid,
            # 'children':[child.to_dict() for child in self.children]
        }

#商品属性
class Attribute(db.Model):
    __tablename__='t_attribute'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(64),nullable=True)
    val=db.Column(db.String(128),nullable=True)
    _type=db.Column(db.Enum('static', 'dynamic'),nullable=True)
    cid=db.Column(db.Integer,db.ForeignKey('t_category.id'),default=1)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'val':self.val,
            '_type':self._type,
            'cid':self.cid,
        }
class Product(db.Model):
    __tablename__ = 't_product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(512), nullable=False)
    price = db.Column(db.Float, default=0)
    number = db.Column(db.Integer, default=0)
    introduce = db.Column(db.Text) # 商品介绍
    big_img = db.Column(db.String(255)) # 商品大图
    small_img = db.Column(db.String(255)) # 商品小图
    state = db.Column(db.Integer) #0未通过 1审核中 2已通过
    is_promote = db.Column(db.Integer) # 是否促销
    hot_number = db.Column(db.Integer) # 热度
    weight = db.Column(db.Integer) # 权重

    cid_one = db.Column(db.Integer, db.ForeignKey('t_category.id'))
    cid_two = db.Column(db.Integer, db.ForeignKey('t_category.id'))
    cid_three = db.Column(db.Integer, db.ForeignKey('t_category.id'))

    category = db.relationship('Category', foreign_keys=[cid_three])

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    def to_dict(self):
        return {
        'id': self.id,
        'name': self.name,
        'price': self.price,
        'number': self.number,
        'introduce': self.introduce,
        'big_img': self.big_img,
        'small_img': self.small_img,
        'state': self.state,
        'is_promote': self.is_promote,
        'hot_number': self.hot_number,
        'weight': self.weight,
        'cid_one': self.cid_one,
        'cid_two': self.cid_two,
        'cid_three': self.cid_three,
        'category': [a.to_dict() for a in self.category.attrs],
        }

class Picture(db.Model):
    __tablename__="t_picture"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    path=db.Column(db.String(255))
    pid=db.Column(db.Integer,db.ForeignKey("t_product.id"))
    


    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

class ProductAttr(db.Model):
    __tablename__="t_pro_attr"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    pid=db.Column(db.Integer,db.ForeignKey("t_product.id"))
    aid=db.Column(db.Integer,db.ForeignKey("t_attribute.id"))
    val=db.Column(db.String(255))
    _type=db.Column(db.Enum("static","dynamic"))

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
class Order(db.Model,BaseModel):
    __tablename__="t_order"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    price=db.Column(db.Float,default=0)
    number=db.Column(db.Integer,default=0)
    pay_status=db.Column(db.Integer,default=0)
    is_send=db.Column(db.Integer,default=0)
    fapiao_title=db.Column(db.String(255))
    fapiao_content=db.Column(db.String(255))
    address=db.Column(db.String(255))
    uid=db.Column(db.Integer,db.ForeignKey('t_user.id'))

    user=db.relationship('User',foreign_keys=[uid])
    order_detail = db.relationship('OrderDetail', backref='order')
    express = db.relationship('Express', backref='order')

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    def to_dict(self):
        return {
        'id': self.id,
        'price': self.price,
        'number': self.number,
        'pay_status': self.pay_status,
        'is_send': self.is_send,
        'fapiao_title': self.fapiao_title,
        'fapiao_content': self.fapiao_content,
        'address': self.address,
        'uid': self.uid,
        'user': self.user.nick_name,
        }


class OrderDetail(db.Model):
    __tablename__='t_order_detail'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    oid=db.Column(db.Integer,db.ForeignKey("t_order.id"))
    pid=db.Column(db.Integer,db.ForeignKey("t_product.id"))
    price=db.Column(db.Float,default=0)
    number=db.Column(db.Integer,default=0)
    total_price=db.Column(db.Float,default=0)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    def to_dict(self):
        return {
        'id': self.id,
        'oid': self.oid,
        'pid': self.pid,
        'number': self.number,
        'price': self.price,
        'total_price': self.total_price,
        }

class Express(db.Model):
    '''快递表'''
    __tablename__ = 't_express'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oid = db.Column(db.Integer, db.ForeignKey('t_order.id'))
    content = db.Column(db.String(256))
    update_time = db.Column(db.String(256))

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    def to_dict(self):
        return {
        'id': self.id,
        'oid': self.oid,
        'content': self.content,
        'update_time': self.update_time,
        }

