from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import time, os
from django.contrib.auth.hashers import make_password, check_password
from django.core.urlresolvers import reverse
from .. import models
from shop.settings import BASE_DIR
from django.core.paginator import Paginator

# Create your views here.
# 用户列表
def vipuser(request):
    # 查询库里的所有数据
    info = models.Users.objects.all().exclude(status=3)

     # 接受类型
    types = request.GET.get('type')
    # 接受关键字
    search = request.GET.get('search')
    # 判断用是否搜索内容
    if types:
        if types=='all':
            #根据id username phone
            # select * from myadmin_users where id like %search% or username like %search% or phone like %search%
            from django.db.models import Q

            info = models.Users.objects.filter(Q(id__contains=search)|Q(username__contains=search)|Q(phone__contains=search))
        elif types=='uname':
            info = models.Users.objects.filter(username__contains=search)
        elif types=='uphone':
            info = models.Users.objects.filter(phone__contains=search)
        elif types == 'uid':
            info = models.Users.objects.filter(id__contains=search)

    # 实例化分页对象
    p = Paginator(info, 10)

    # 一共可以分几页
    sumpage = p.num_pages

    # 取第几页的数据
    # 接收用户的页码
    page = int(request.GET.get('p', 1))
    # 第几页的数据
    page1 = p.page(page)

    if page <= 3:
        # 页码的迭代序列  [1,2,3,4,5,6,7]
        prange = p.page_range[:5]
    elif page + 2 >= sumpage:
        prange = p.page_range[-5:]
    else:
        prange = p.page_range[page - 3: page + 2]


    return render(request,'myadmin/table-list.html',{'info':page1,'prange':prange,'page':page,'sumpage':sumpage})


def adduser(request):
    if request.method == 'GET':
        return render(request, 'myadmin/adduser.html')
    elif request.method == 'POST':

        userinfo = request.POST.dict()
        userinfo.pop('csrfmiddlewaretoken')
        print(userinfo)

        myfile = request.FILES.get('head_url') # ###

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

def deluser(request):
    uid = request.GET.get('uid')
    user = models.Users.objects.get(id=uid)
    user.status = 3
    user.save()
    return redirect(reverse('myadmin_vipuser'))

def edituser(request):
    # 接受用户的id
    uid = request.GET.get('uid')
    # 判断是get还是post
    if request.method == 'GET':
        user = models.Users.objects.get(id=uid)
        return render(request, 'myadmin/edit.html', {'userinfo': user})
    elif request.method == 'POST':
        # 获取用户的提交信息
        userinfo = request.POST.dict()
        # 更新数据
        uinfo = models.Users.objects.get(id=uid)
        uinfo.username = userinfo['username']
        uinfo.phone = userinfo['phone']
        uinfo.age = userinfo['age']
        uinfo.sex = userinfo['sex']
        # 判断头像有没有上传
        file = request.FILES.get('head_url')
        if file:
            # 右头像上传，要吧旧投头像删除
            # /dajngo07/py17/shop    ./static/pics/1547686265.6370358.png
            os.remove('.' + uinfo.head_url)
            headurl = upload(file)
            uinfo.head_url = headurl
        uinfo.save()
        return redirect(reverse('myadmin_vipuser'))

        
# 修改状态
def changes(request):
    # 获取uid 获取状态值
    uid = request.GET.get('uid')
    status = request.GET.get('status')
    try:
        user = models.Users.objects.get(id=uid)
        user.status = int(status)
        user.save()
        msg = {'msg': '修改状态成功'}
        return JsonResponse(msg)
    except:
        msg = {'msg': '修改状态失败'}
        return JsonResponse(msg)    

# 重置密码
def respwd(request):
    # 
    uid = request.GET.get('uid')
    user = models.Users.objects.get(id=uid)
    user.password = make_password('123456', None, 'pbkdf2_sha256')
    user.save()
    # res = check_password('123456', 'pbkdf2_sha256$36000$hZvkItMm9w48$Xoxa4liNA2kigCW9FFquzfh3ppa1VCal50Zfoyu1ii0=')
    # print(res)
    data = {'msg': '重置密码成功'}
    return JsonResponse(data)

# 封装成函数
def upload(myfile):
    """
    参数:上传的文件名
    功能:头像文件上传到后台
    返回值:头像文件路径在项目的完整路径
    """
    # 新名字
    filename = str(time.time()) + '.' + myfile.name.split('.').pop()
    destination = open("./static/pics/" + filename, "wb+")
    for chunk in myfile.chunks(): # 分块写入文件
        destination.write(chunk)
    destination.close()
    # /static/pics/filename
    return '/static/pics/' + filename