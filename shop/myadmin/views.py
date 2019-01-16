from django.shortcuts import render, redirect
from django.http import HttpResponse
import time, os
from django.contrib.auth.hashers import make_password, check_password
from django.core.urlresolvers import reverse
from . import models

# Create your views here.
def index(request):
    return render(request, 'myadmin/index.html')

# 用户列表
def vipuser(request):

    return render(request, 'myadmin/table-list.html')

def adduser(request):
    if request.method == 'GET':
        return render(request, 'myadmin/adduser.html')
    elif request.method == 'POST':

        userinfo = request.POST.dict()
        userinfo.pop('csrfmiddlewaretoken')
        print(userinfo)

        myfile = request.FILES.get('head_url')

        if not myfile:
            return HttpResponse("<script>alert('请选择头像'); location.href = '';</script>")

        userinfo['head_url'] = upload(myfile)

        userinfo['password'] = make_password(userinfo['password'], None, 'pbkdf2_sha256')
        
        try:
            user = models.Users(**userinfo)
            user.save()
            return redirect(reverse('myadmin_vipuser'))        
        except:
            return HttpResponse("<script>alert('添加失败!!'); location.href = '';</script>")
# 封装成函数
def upload(myfile):
    """
    功能:头像文件上传
    """
    # 新名字
    filename = str(time.time()) + '.' + myfile.name.split('.').pop()
    destination = open("./static/pics/" + filename, "wb+")
    for chunk in myfile.chunks(): # 分块写入文件
        destination.write(chunk)
    destination.close()
    # /static/pics/filename
    return 'static/pics' + filename