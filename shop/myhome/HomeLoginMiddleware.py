from django.shortcuts import render
from django.http import HttpResponse
import re

class HomeLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        lists = ['/login/', '/'] # 在没有登录的情况下,只有这两条路由可以访问
        if re.match('/', path) and path not in lists:
            if request.session.get('userinfo', '') == '':
                return HttpResponse('<script>alert("请先登录");location.href="/login/";</script>')
        
        response = self.get_response(request)
        return response                     