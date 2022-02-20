from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models  import *
from user.models import *

# Create your views here.
#装饰器校验登陆状态
def Check_login(f):
    def wrap(request,*args,**kwargs):

        #检查session
        if (not request.session.get('username')) or (not request.session.get('uid')):

            #检查COOKIES
            c_username=request.COOKIES.get('username')
            c_uid=request.COOKIES.get('uid')
            if (not c_username) or (not c_uid):

                #返回登陆界面
                return HttpResponseRedirect("/user/login")
            else:
                #回写session
                request.session['username']=c_username
                request.session['uid']=c_uid

            #如果有登陆状态（session 有内容）,进入笔记页面
        return f(request,*args,**kwargs)
    return wrap


@Check_login
def list_view(request):

    #从session里取出登陆者的user.id
    uid=request.session.get('uid')
    username = request.session.get('username')
    #根据登陆者的id通过外键查寻对应的note(返回值对象类list)
    someone_note = Note.objects.filter(user_id=uid,is_active = True)

    return render(request,'note/list_note.html',locals())


@Check_login
def add_note(request):
     if request.method == 'GET':
         return render(request,'note/add_note.html')

     if request.method == 'POST':

        #存储笔记数据
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']

        Note.objects.create(title=title,content=content, user_id=uid)

        return HttpResponseRedirect('/note/all')


@Check_login
def updated_note(request,note_id):

    #获取需要修改的那一行数据（object）
    try:
        note = Note.objects.get(id = note_id,is_active = True)
    except Exception as e:
        print('__updated note error is %s' % (e))
        return HttpResponse("__The note is not exited")


    if request.method == 'GET':
        return render(request,'note/updated_note.html',locals())


    if request.method == 'POST':

    #存储笔记数据
        note.title = request.POST['title']
        note.content = request.POST['content']

        note.save()

        return HttpResponseRedirect('/note/all')


@Check_login
def delete_note(request):

    note_id=request.GET.get('note_id')

    if not note_id:
        return HttpResponse('exception')

    try:
        note = Note.objects.get(id=note_id,is_active = True)
    except Exception as e:
        print('__updated note error is %s' % (e))
        return HttpResponse("__The note is not exited")

    note.is_active = False
    note.save()
    return HttpResponseRedirect('/note/all')