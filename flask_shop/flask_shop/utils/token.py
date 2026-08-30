
'''
1.要加密的数据
   userid

2.密钥的算法
    pip install pyjwt=2.6.0

3.加密的密钥

'''
from jwt import encode, decode
from flask import current_app
from time import time
from functools import wraps
from flask import request

# 生成token
def generate_token(data):
    # 生成token
    data.update({'exp':time()+current_app.config['TOKEN_EXPIRED']})
    token=encode(data,current_app.config['SECRET_KEY'],algorithm='HS256')

    return token

# 解密token
def parse_token(token):
    try:
    # 解密token
        data=decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
        return data
    except Exception as e:
        return None

def login_required(view_func):
    @wraps(view_func)
    def parse_token_info(*args,**kwargs):
       token=request.headers.get('token')
       if not token:
           return '请登录！'
       data=parse_token(token)
       if not data:
           return {'code': 401, 'msg': 'token 已过期'}
       return view_func(*args,**kwargs)
    return parse_token_info
        