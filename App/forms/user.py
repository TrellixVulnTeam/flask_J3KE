from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, EqualTo, Email, ValidationError, DataRequired

# 定义用户注册表单类,注册用，与别数据库的models
from App.models import User


class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[Length(4,20,message='用户名必须在4~20字符之间')])
    password = PasswordField('密码', validators=[Length(6,20,message='密码必须在6~20字符之间')])
    confirm = PasswordField('密码确认',validators=[EqualTo('password',message='密码必须保持一致')])
    email = StringField('邮箱',validators=[Email(message='请输入正确的邮箱格式')])
    submit = SubmitField('提交')


    # 自定义验证-必须
    def validate_username(self,field):
        u = User.query.filter_by(username=field.data).first()
        if u:
            raise ValidationError('用户已存在')
    # 邮箱校验
    def validate_email(self,field):
        u = User.query.filter_by(email=field.data).first()
        if u:
            raise ValidationError('邮箱用户已存在')

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    remenber = BooleanField('记住我',default=False)
    submit = SubmitField('提交')



