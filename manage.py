# coding:utf-8
from flask import Flask, render_template
from flask_script import Manager
from App import create_app
import os
from flask_migrate import MigrateCommand
# 从环境变量中获取config_name
config_name = os.environ.get('FLASK_CONFIG') or 'default'

# 创建app实例
app = create_app(config_name)
manager = Manager(app)
manager.add_command('db',MigrateCommand)#取名




if __name__ == '__main__':
    manager.run()







