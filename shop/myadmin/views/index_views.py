from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
import time, os
from django.core.urlresolvers import reverse
from .. import models
from shop.settings import BASE_DIR
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request, 'myadmin/index.html')