from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
import hashlib

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

        # 2.当前用户名是否可用
        users = User.objects.filter(username=username)
        if users:
            return HttpResponse('你的用户名已经存在，请重新输入')

        # 密码加密（hash -md5）
        # hash 密码 特点：
        # 1：定长输出：无论是输入多少，哈希值定长：md5 32位16进制
        # 2：不可逆：无法反向计算出明文
        # 3.雪崩效应： 输入改变，输出一定改变
        # 一般用于密码处理和文件完整性校验
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()

        #创建账号（插入数据）
        #优化：并发插入防报错
        try:
            user=User.objects.create(username=username,password=password_m)
        except Exception as e:
            print('——create user errors %s'%(e))
            return HttpResponse('该用户已被注册')

        #免登陆一天
        request.session['username']=username
        request.session['uid']=user.id
        #TO DO 在修改时间为1天

        #return HttpResponse('注册成功')
        return HttpResponseRedirect('/index')


def login_view(request):
    if request.method=="GET":

        #获取登陆页面
        #检查是否最近登陆过
        if request.session.get('username') and request.session.get('uid'):
            #return HttpResponse('已登录')
            return HttpResponseRedirect('/index')

        #检查Cookies
        c_username=request.COOKIES.get('username')
        c_uid=request.COOKIES.get('uid')
        if c_uid and c_username:
            request.session['username']=c_username
            request.session['uid']=c_uid
            #return HttpResponse('已登录')
            return HttpResponseRedirect('/index')

        return render(request,'user/login.html')
    elif request.method=="POST":

        #取出用户提交的数据
        username=request.POST['username']
        password=request.POST['password']
        m=hashlib.md5()
        m.update(password.encode())
        password_u=m.hexdigest()

        #取出数据库里的用户数据
        try:
            user=User.objects.get(username=username)
        except Exception as e:
            print('--login user error %s' %(e))
            return HttpResponse('你的密码或账号输入出错，请重新输入')
        else:
            password_m = user.password

        #对比两种数据
        if password_u != password_m:
            return HttpResponse('你的密码或账号输入出错，请重新输入')

        #resp = HttpResponse('成功登陆！')
        resp=HttpResponseRedirect('/index')

        #存储session
        request.session['username']=username
        request.session['uid']=user.id

        #判断是否勾选了“记住用户”
        #有就存储在Cookies 里面3天
        if request.POST.get('remember'):
            resp.set_cookie('username',username,3600*24*3)
            resp.set_cookie('uid',user.id, 3600 * 24 * 3)

        return resp


def logut_view(request):

    #删除session
    del request.session['username']
    del request.session['uid']

    resp=HttpResponseRedirect('/index')

    #删除COOKIES
    resp.delete_cookie('username')
    resp.delete_cookie('uid')

    return resp



