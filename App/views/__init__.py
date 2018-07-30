
# 用于Blueprint注册



#定义一个元组，存放蓝本的配置
from .main import main
from .user import user

DEFAULT_BLUEPRINT = (
    (main,''),
    (user,'/user'),


)

# 定义注册蓝本的函数
def config_blueprint(app):
    for blueprint,prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint,url_prefix = prefix)# 可以加前缀
















