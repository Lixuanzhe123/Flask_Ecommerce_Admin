# Flask 电商后台管理系统

一个前后端分离的电商后台管理项目。后端使用 Flask、Flask-RESTful、SQLAlchemy 和 MySQL 提供 REST API，前端使用 Vue 3、Element Plus、ECharts 和 TinyMCE 构建管理界面。

## 主要功能

- 管理员登录与 JWT 身份认证
- 用户列表、添加、编辑、删除和密码重置
- 角色管理、菜单权限和角色授权
- 商品分类与分类级联管理
- 商品属性分组和属性维护
- 商品列表、商品详情、图片上传与富文本编辑
- 订单列表、订单详情和物流信息查询
- 首页数据统计与 ECharts 可视化
- Vue Router 页面路由和 Axios 请求封装

## 技术栈

### 后端

- Python / Flask
- Flask-RESTful
- Flask-SQLAlchemy / Flask-Migrate
- MySQL / PyMySQL
- JWT / Flask-Cors

### 前端

- Vue 3 / Vue Router 4
- Element Plus
- Axios
- ECharts
- TinyMCE

## 项目结构

```text
Flask电商后台项目/
├─ flask_shop/                 # Flask 后端
│  ├─ flask_shop/
│  │  ├─ user/                # 用户接口
│  │  ├─ roles/               # 角色和授权接口
│  │  ├─ menu/                # 菜单接口
│  │  ├─ group/               # 分类与属性接口
│  │  ├─ product/             # 商品接口
│  │  ├─ order/               # 订单接口
│  │  ├─ utils/token.py       # JWT 工具
│  │  └─ models.py            # 数据模型
│  ├─ migrations/             # Alembic 数据库迁移
│  ├─ config.py               # 环境变量配置
│  └─ manage.py               # 后端启动入口
├─ vue_shop/                   # Vue 管理后台
│  ├─ src/views/              # 业务页面
│  ├─ src/api/                # API 地址
│  ├─ src/utils/request.js    # Axios 封装
│  └─ public/tinymce/         # 富文本编辑器资源
└─ .env.example               # 配置示例
```

## 本地运行

### 1. 配置数据库

创建 MySQL 数据库 `flask_shop`，然后复制环境变量示例并填写连接信息：

```powershell
Copy-Item .env.example .env
```

### 2. 启动 Flask 后端

```powershell
cd flask_shop
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = "manage.py"
flask db upgrade
python manage.py
```

后端默认运行在 `http://localhost:5000`。

### 3. 启动 Vue 前端

```powershell
cd vue_shop
yarn install
yarn serve
```

前端 API 默认访问 `http://localhost:5000`。

生产构建：

```powershell
yarn build
```

