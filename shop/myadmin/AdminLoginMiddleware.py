from django.shortcuts import render
from django.http import HttpResponse
import re


class AdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # 1.接受用户的请求路径
        path = request.path

        # 2.验证用户是否访问的是myadmin/ 并且访问不是登录页面
        #  127.0.0.1:8000/myadmin/logoin/
        lists = ['/myadmin/login/', '/myadmin/verifycode/']
        if re.match('/myadmin/', path) and path not in lists:
            # 判断有没有登录 如果没有登返回到登录页面
            if request.session.get('adminuser', '') == '':
                return HttpResponse('<script>alert("请先登录");location.href="/myadmin/login";</script>')

        response = self.get_response(request)
        return response               