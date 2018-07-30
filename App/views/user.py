from flask_login import login_user,logout_user,login_required

from App.models import User
from flask import Blueprint, render_template, flash, redirect, url_for, request
from App.forms import RegisterForm, LoginForm
from App.extensions import db
from App.email import send_mail
user = Blueprint('user',__name__)

@user.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    # post才能进
    if form.validate_on_submit():# 此段代码可优化，不够简洁
        #判断用户存不存在
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash('亲，账号或密码输错了呀~')
            return render_template('user/login.html',form=form)
        #存在在判断密码是否相等,用models里边的方法验证
        if not u.verify_password(form.password.data):
            flash('亲，账号或密码输错了呀~')
        #登录写入session
        # 此处需要用到第三方包pip install flask-login,并且在ext进行初始化,
        # 并且需要一个认证的回调函数，写在user model中
        login_user(u,remember=form.remenber.data)#需要导入，然后看底层的东西， 记住我
        #登录成功返回首页，或者之前野蛮
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('user/login.html',form=form)

@user.route('/register/',methods=['GET','POST'])
def register():
    form =RegisterForm()
    if form.validate_on_submit():
        #根据数据生成对象
        u = User(username = form.username.data,
                 email = form.email.data,
                 password = form.password.data,
                 )
        print('*'*50)
        print(u.username)
        #保存对象
        db.session.add(u)
        # 必须提交
        db.session.commit()

        token = u.generate_activate_token()
        send_mail('Paddy论坛账户激活',form.email.data,'user/activate',
                  username=form.username.data,token=token)
        flash('邮件已发送，请点击链接完成用户激活')
        #跳转页面
        return redirect(url_for('main.index'))
    return render_template('user/register.html',form=form)
''''
用户注册的时候，由用户生成一个包含用户自身id信息和过期时间信息的token
并在发送邮件的时候，一并把这个token发送到邮件中。
用户点击邮件的url地址后，跳转到处理激活的视图中。
接收这个token，并对这个token进行解析
解析的思路，就是提取这个token中的uid，根据uid能否找到对象。
生成的函数放在models的user
'''
# 激活跳转到这里
@user.route('/activate/<token>')# 我的天哪！！这里需要参数,不要后面的/
def activate(token):
    # 解密用了静态方法，所以用的类名
    # 判断返回的是true false即成功与否
    if User.check_activate_token(token):
        flash('激活成功')
        # 跳转首页
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        # 为了与视频一致，此处暂时跳转至首页
        return redirect(url_for('main.index'))
        # 跳转注册界面
       # return render_template(url_for('user.register'))
#退出登录
@user.route('/logout/')
def logout():
    logout_user()
    flash('用户已退出')
    return redirect('main.index')

# 路由保护，比如登录才能访问,有需要可以用
# 没登录会调到登录界面，ext里设置
@user.route('/test/')
@login_required
def test():
    # 跳转之前的页面或者主页
    return redirect(request.args.get('next') or url_for('main.index'))


@user.route('/profile/')
def profile():
    return render_template('user/profile.html')