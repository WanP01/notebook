from django.db import models

# Create your models here.

#用户的密码/账号格式
class User(models.Model):
    username=models.CharField('username',max_length=30)
    password=models.CharField('password',max_length=32)
    create_time=models.DateTimeField('Create_time',auto_now_add=True)
    updated_time=models.DateTimeField('updated_time',auto_now=True)

    def __str__(self):
        return 'username %s'%(self.username)
