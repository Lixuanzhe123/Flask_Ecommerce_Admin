import os

#pip install Flask-SQLAlchemy
#pip install pymysql
#pip install flask-migrate
# pip install flask

from flask_migrate import Migrate
from flask_cors import CORS

from flask_shop import create_app,db


app=create_app(os.getenv("FLASK_CONFIG", "dev"))
app.url_map.strict_slashes = False
CORS(app, resources=r'/*', origins='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])#允许跨域
#创建同步数据库
Migrate(app,db)

'''
flask db init#初始化
flask db migrate#生成迁移文件
flask db upgrade#同步数据库
'''

if __name__=='__main__':
    app.run()
