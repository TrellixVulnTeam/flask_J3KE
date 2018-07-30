from App.config import  config
from flask import Flask, render_template
from App.extensions import config_extensions
from App.views import config_blueprint

# 配置错误界面
def config_errorhandler(app):
    @app.errorhandler(404)
    def error_h(e):
        return render_template('erros/404.html')

# 封装一个函数，创建app
def create_app(config_name):
    # 生成app实例
    app =Flask(__name__)
    # 读取配置,返回的是类
    app.config.from_object(config.get(config_name) or config['default'])

    # 执行额外的初始化操作,调用静态函数
    config[config_name].init_app(app)

    # 添加扩展
    config_extensions(app)
    # 配置蓝本
    config_blueprint(app)

    # 配置错误界面
    config_errorhandler(app)

    #返回app
    return app






