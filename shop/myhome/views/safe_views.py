from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from myadmin import models
from django.core.urlresolvers import reverse
import os,time
from shop.settings import BASE_DIR
# xuyaping

# 账户安全
def safety(request):
    user = models.Users.objects.get(id=request.session['userinfo']['uid'])
    print(user)

    data = {
        'user': user,
    }
    return render(request, 'myhome/safety.html', data) 

# 账户安全-登录密码
def resetpwd(request):
    if request.method == 'GET':
        return render(request, 'myhome/password.html')
    elif request.method == 'POST':
        data = request.POST.dict() # 拿到的数据
        print(data)
        
        user = models.Users.objects.get(id=request.session['userinfo']['uid']) # 當前用戶
        # print(user.password) # 旧密码

        user.password = make_password(data['pwd2'], None, 'pbkdf2_sha256') # 新密碼
        print(user.password)
        user.save()

        # return HttpResponse('ok')
        return HttpResponse('<script>alert("修改成功,请重新登录");location.href="' + reverse('myhome_login') + '";</script>')

# ajax验证旧的密码 
def verifyold(request):
    # 密码验证
    oldpwd = request.GET.get('oldpwd')
    print(oldpwd)
    user = models.Users.objects.get(id=request.session['userinfo']['uid']) # 當前用戶

    upass = check_password(oldpwd, user.password)
    # 判断密码是否正确
    if upass:
        return JsonResponse({'msg': '成功', 'error': 0})
    else:
        return JsonResponse({'msg': '失败', 'error': 1})

# 换绑手机
def bindphone(request):
    if request.method == 'GET':
        user = models.Users.objects.get(id=request.session['userinfo']['uid'])
        return render(request, 'myhome/bindphone.html', {'user': user})
    elif request.method == 'POST':
        phone = request.POST.get('newphone')
        print(newphone)
        
        return HttpResponse('ok')

# 验证码接口
def sendmsg(request):
    import urllib
    import urllib.request
    import json
    import random
    #用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    account  = "C87000499" 
    #密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "b485a61d820183a8058bf15b717e925b"
    mobile = request.GET.get('phone')
    # 随机验证码
    code = str(random.randint(10000,99999))
    # 把验证码存入session
    request.session['msgcode'] = {'code':code,'phone':mobile}
    print(code)
    return JsonResponse({'code':code})
