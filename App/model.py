from ext import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),index=True)
    age = db.Column(db.Integer,default=20)
    sex = db.Column(db.Boolean,default=True)
    info = db.Column(db.String(50))


    def __init__(self,username,age=20,sex=False,info='个人简介'):
        self.username = username
        self.age = age
        self.sex = sex
        self.info = info


