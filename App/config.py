import os
base_dir = os.path.abspath(os.path.dirname(__file__))
# 通用配置
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  or '123456'
    # 数据库,第一行设置自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True #提交时不需要 db.commit()
    SQLALCHEMY_TRACK_MODIFICATIONS = False #忽略系统警告
    # 邮件发送
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '13510069294@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'abc1234'
    #额外的初始操作
    @staticmethod
    def init_app(self):
        pass


# 开发环境
class DevelopmentConfig(Config):
    # 数据库连接
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(base_dir,'blog-dev.sqlite')

# 测试环境
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(base_dir,'blog-dev.sqlite')
#生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(base_dir,'blog-dev.sqlite')

# 配置字典
config = {
    'development':DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig

}






