class Config(object):
    DEBUG = False
    TESTING = False
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'gamdwk'
    PASSWORD = 'gamdwk'
    HOST = 'localhost'
    PORT = '3306'
    DATABASE = 'seaflow'
    SECRET_KEY = b'1x\xd7\xdeu\x96\x80\xfc{#\xec9\xdb\x99\xc2\xf6'
    # 配置flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 自动提交
    # 配置flask-mail
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USERNAME = '728882065@qq.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = ("seaflow", "728882065@qq.com")
    # flask-bcrypt
    BCRYPT_LOG_ROUNDS = 12
    UPLOAD_PATH = '/www/wwwroot/static'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
