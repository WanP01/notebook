from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def reg_view(request):

    #获取请求
    if request.method=="GET":
        return render(request,'user/register.html')
    #获得提交的表单
    elif request.method=="POST":
        username= request.POST['username']
        password=request.POST['password']
        password_2=request.POST['password_2']

        #1.密码是否一致
        if password != password_2:
            return HttpResponse('你的密码输入不一致')
        users = User.objects.filter(username=username)

        # 2.当前用户名是否可用
        if users:
            return HttpResponse('你的用户名已经存在，请重新输入')

        #创建账号（插入数据）
        User.objects.create(username=username,password=password)
        return HttpResponse('注册成功')
