from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required

# 管理员用户添加
def useradd(request):
    if request.method == 'GET':
        # 获取所有的组
        glist = Group.objects.all()
        context = {'glist': glist}
        # 显示添加页面
        return render(request, 'auth/user/add.html', context)

    elif request.method == 'POST':
        # 执行管理员添加
        
        # 判断是否创建超级管理员
        if request.POST['is_superuser'] == '1':
            ob = User.objects.create_superuser(request.POST['username'], request.POST['email'], request.POST['password'])
        else:
            ob = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        # 进行添加
        ob.save()

        # 判断是否需要为用户分配组
        gs = request.POST.getlist('gs', None)
        if gs:
            # 给当前用户分组
            ob.groups.set(gs)
            ob.save()

        return HttpResponse('<script>location.href="/myadmin/auth/user/list"</script>')

# 管理员用户列表
def userlist(request):
    # 获取所有的管理员
    data = User.objects.all()

    context = {'ulist': data}

    return render(request, 'auth/user/list.html', context)

# 管理员删除
def userdel(request, uid):
    ob = User.objects.get(id=uid)
    ob.delete()
    return HttpResponse('<script>location.href="/myadmin/auth/user/list"</script>')


# 管理组添加
def groupadd(request):
    if request.method == 'GET':

        # 读取所有的权限
        perms = Permission.objects.exclude(name__istartswith='Can')
        context = {'perms': perms}
        return render(request, 'auth/group/add.html', context)
    elif request.method == 'POST':
        # 创建组
        g = Group(name=request.POST['name'])
        g.save()

        # 获取选择的所有权限
        prms = request.POST.getlist('prms', None)
        
        # 判断是否需要给组添加权限
        if prms:
            # 给组分配权限
            g.permissions.set(prms)
            g.save()

        return HttpResponse('<script>location.href="/myadmin/auth/group/list"</script>')


# 管理组列表
def grouplist(request):
    # 获取所有的组
    data = Group.objects.all()
    context = {'glist': data}
    return render(request, 'auth/group/list.html', context)

# 编辑组
def groupedit(request, gid):
    # 获取当前组的信息
    ginfo = Group.objects.get(id=gid)

    if request.method == 'GET':
        # 读取所有权限信息,并排除已经有的权限
        perms = Permission.objects.exclude(group=ginfo).exclude(name__istartswith='Can')
        
        context = {'ginfo': ginfo, 'perms': perms}
        return render(request, 'auth/group/edit.html', context)
    elif request.method == 'POST':
        # 修改组名
        ginfo.name = request.POST['name']

        # 判断是否有权限
        prms = request.POST.getlist('prms', None)

        # 全部删除,在添加
        ginfo.permissions.clear()

        if prms:
            # 在添加权限
            ginfo.permissions.set(prms)

        ginfo.save()
        return HttpResponse('<script>location.href="/myadmin/auth/group/list"</script>')


# 登录
def myadminLogin(request):
    if request.method == 'GET':
        return render(request, 'myadmin/login.html')    
    elif request.method == "POST":
        # 接受用户传的参数
        user = request.POST.dict()
        print('+++++++++++++',user)

        # 判断验证码是否正确
        if request.POST['yzm'].lower() != request.session['verifycode'].lower():
            return HttpResponse('<script>alert("验证码错误");location.href="' + reverse('myadmin_login') + '";</script>')

        # 使用django提供的后台用户验证方法
        username = request.POST['name']
        password = request.POST['pwd']
        user = authenticate(request, username=username, password=password)
        if user:
            # 登录
            login(request, user)
            return HttpResponse('<script>location.href="/myadmin/";</script>')
        return HttpResponse('<script>alert("账号或密码错误");location.href="' + reverse('myadmin_login') + '";</script>')

        # # 判断用户名密码
        # if user['name'] == 'admin' and user['pwd'] == '123456':   
        #     if user['yzm'].upper() == request.session.get('verifycode').upper():
        #         #################  用户登陆成功后 将用户信息存入session  ########################
        #         request.session['adminuser'] = {'vipuser': user['name'], 'uid': 1}
        #         return HttpResponse('<script>alert("登录成功");location.href="' + reverse('myadmin_index') + '";</script>')
        #     else:
        #         return HttpResponse('<script>alert("证码错误，重新输入");location.href="' + reverse('myadmin_login') + '";</script>')                
        # else:
        #     return HttpResponse('<script>alert("账号或密码错误");location.href="' + reverse('myadmin_login') + '";</script>')

# 退出登录
def myadminLogout(request):
    # 删除session中存的用户信息
    # request.session['adminuser']={} 或者下面的
    # del request.session['adminuser']
    logout(request)
    return HttpResponse('<script>alert("退出成功");location.href="' + reverse('myadmin_login') + '";</script>') 