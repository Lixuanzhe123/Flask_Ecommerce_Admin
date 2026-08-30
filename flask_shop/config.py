import os
from urllib.parse import quote_plus

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
load_dotenv(os.path.join(BASE_DIR, ".env"))

try:
    import _local_config as _local
except ImportError:
    _local = None


def _local_value(name, default=None):
    if _local is None:
        return default
    return getattr(_local.Config, name, default)


def _env_int(name, default):
    return int(os.getenv(name, default))


class Config:
    MYSQL_DIALECT = os.getenv("SHOP_MYSQL_DIALECT", _local_value("MYSQL_DIALECT", "mysql"))
    MYSQL_DRIVER = os.getenv("SHOP_MYSQL_DRIVER", _local_value("MYSQL_DRIVER", "pymysql"))
    MYSQL_USER = os.getenv("SHOP_MYSQL_USER", _local_value("MYSQL_USER", "root"))
    MYSQL_PASSWORD = os.getenv("SHOP_MYSQL_PASSWORD", _local_value("MYSQL_PASSWORD", ""))
    MYSQL_HOST = os.getenv("SHOP_MYSQL_HOST", _local_value("MYSQL_HOST", "localhost"))
    MYSQL_PORT = _env_int("SHOP_MYSQL_PORT", _local_value("MYSQL_PORT", 3306))
    MYSQL_DB = os.getenv("SHOP_MYSQL_DB", _local_value("MYSQL_DB", "flask_shop"))
    MYSQL_CHARSET = os.getenv("SHOP_MYSQL_CHARSET", _local_value("MYSQL_CHARSET", "utf8mb4"))

    SQLALCHEMY_DATABASE_URI = os.getenv("SHOP_DATABASE_URI") or (
        f"{MYSQL_DIALECT}+{MYSQL_DRIVER}://"
        f"{quote_plus(MYSQL_USER)}:{quote_plus(MYSQL_PASSWORD)}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset={MYSQL_CHARSET}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SHOP_SECRET_KEY", _local_value("SECRET_KEY", os.urandom(16)))
    DEBUG = False
    JSON_AS_ASCII = False
    RESTFUL_JSON = {"ensure_ascii": False}
    USE_RELOADER = False
    TOKEN_EXPIRED = _env_int("SHOP_TOKEN_EXPIRED", _local_value("TOKEN_EXPIRED", 86400))
    APPEND_SLASH = False

    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
    BASE_DIR = BASE_DIR
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "flask_shop", "static", "upload")


class TestConfig(Config):
    DEBUG = True


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False


config_map = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig,
}
