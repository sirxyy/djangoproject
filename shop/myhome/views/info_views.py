from django.shortcuts import render
from django.http import HttpResponse


def myhome_info(request):
    return render(request, 'myhome/goodsinfo.html')