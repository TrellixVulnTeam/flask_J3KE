from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import  FlaskForm
from flask_uploads import UploadSet
from flask_login import LoginManager



# 创建扩展

bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
db = SQLAlchemy()
# def init_app(self, app, db=None, directory=None, **kwargs):
migrate = Migrate(db=db)
login_manager = LoginManager()

# 初始化
def config_extensions(app):
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app)


    ######loging_manager专区##
    #配置login_manager
    login_manager.init_app(app)
    # 指定登录的端点/路由
    login_manager.login_view='user.login'
    # 需要登陆才能访问的提示信息
    login_manager.login_message='请先登录才能访问呢'
    # 设置session保护级别
    #None:禁用session保护
    #'basic':基本的保护，默认选项
    # 'strong'最严格的保护，一单用户登陆信息改变立即退出登录
    login_manager.session_protection='strong'

