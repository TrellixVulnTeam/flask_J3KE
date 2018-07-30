from App.extensions import db
# 用于加密密码
from werkzeug.security import generate_password_hash,check_password_hash
# 用于token生成
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# 用于判断token是否过期，看单词也能了解
from itsdangerous import SignatureExpired,BadSignature

from flask import current_app, flash
# flask-login专属
from App.extensions import login_manager
from flask_login import UserMixin

class User(db.Model,UserMixin):# 给user增加额外的属性方法
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True)
    confirmed = db.Column(db.Boolean,default=False)


    #设置密码不能直接访问
    @property
    def password(self):
        raise AttributeError('密码不能直接访问')
    # 设置密码,是函数名.setter
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    # 校验密码
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
# python manage.py db init生成migration
#python manage.py db  migrate
#python manage.py db upgrade
# 使用sqlite数据库


# 生成激活的token
    def generate_activate_token(self):
        #def __init__(self, secret_key, expires_in=None, **kwargs):
        # expires默认3600秒
        #TimedJSONWebSignatureSerializer时间jsonweb签名序列化
        s=Serializer(current_app.config['SECRET_KEY'],expires_in=3600)
        return s.dumps({'uid':self.id})

    #解密token
    @staticmethod
    def check_activate_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        # 判断token是否过期或者合法
        try:
            data = s.loads(token)
        except BadSignature:
            flash('非法的token')
            return False
        except SignatureExpired:
            flash('token已过期')
            return False
        u = User.query.get(int(data['uid']))#取出当前用户id的对象
        # 判断用户存在不存在
        if not u:
            flash('用户不存在')
            return False
        # 判断是否激活过
        if u.confirmed:
            flash('用户已激活')
            return False
        u.confirmed=True
        # 用于提交
        db.session.add(u)
        return True

# 获取user的回调函数---用于flask-login，current_user
@login_manager.user_loader
def user_loader(uid):
    return User.query.get(uid)