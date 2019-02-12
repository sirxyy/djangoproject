from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from .. import models
from .import cate_views, user_views
from django.core.paginator import Paginator
import time,os, os.path
from django.contrib.auth.decorators import permission_required

# 添加
@permission_required('myadmin.insert_goods', raise_exception=True)
def addgoods(request):
    # 查询所有的分类  进行返回
    types = cate_views.tab()
    return render(request, 'myadmin/goods/addgoods.html', {'types': types})

# 添加数据
@permission_required('myadmin.insert_goods', raise_exception=True)
def goodsinsert(request):
    # 接受用户的信息
    ginfo = request.POST.dict()
    print(ginfo)

    ginfo.pop('csrfmiddlewaretoken')
    print(ginfo)

    file = request.FILES.get('g_url')
    if not file:
        return HttpResponse('<script>alert("请选择图片");history.back(-1);</script>')

    # 调图片上传
    g_url = user_views.upload(file)

    # 入库
    goods = models.Goods()
    goods.title = ginfo['title']
    goods.ordernum = ginfo['ordernum']
    goods.g_url = g_url
    goods.price = ginfo['price']
    goods.ginfo = ginfo['ginfo']
    goods.cateid = models.Cates.objects.get(id=ginfo['cateid'])
    goods.save()
    # print('++++++++++++++++++', goods)

    return HttpResponse('<script>location.href="http://127.0.0.1:8000/myadmin/addgoods/";</script>')    

@permission_required('myadmin.show_goods', raise_exception=True)
def goodslist(request):
    goods = models.Goods.objects.all()

    # all
    # id
    # title
    # price
    # ordernum
    types = request.GET.get('type')
    search = request.GET.get('search')
    if types:
        if types == 'all':
            from django.db.models import Q
            goods = models.Goods.objects.filter(Q(id__contains=search)|Q(title_contains=search)|Q(price__contains=search)|Q(ordernum__contains=search))
        elif types == 'id':
            goods = models.Goods.objects.filter(id__contains=search)
        elif types == 'title':
            goods = models.Goods.objects.filter(title__contains=search)
        elif types == 'price':
            goods = models.Goods.objects.filter(price__contains=search)
        elif types == 'ordernum':
            goods = models.Goods.objects.filter(ordernum__contains=search)

    # goods = models.Goods.objects.all()

    p = Paginator(goods, 2)

    sumpage = p.num_pages

    page = int(request.GET.get('p', 1))

    page1 = p.page(page)

    if page <= 3:
        prange = p.page_range[:5]
    elif page + 2 >= sumpage:
        prange = p.page_range[-5:]
    else:
        prange = p.page_range[page - 3, page + 2]
        

    return render(request, 'myadmin/goods/goodlist.html', {'goods': page1, 'prange': prange, 'page': page, 'sumpage': sumpage})


@permission_required('myadmin.del_goods', raise_exception=True)
def delgoods(request):
    gid = request.GET.get('gid')
    print(gid)
    try:
        goods = models.Goods.objects.get(id=gid)
        print(goods)
        goods.delete()
        return JsonResponse({'msg': '1'})
    except:
        return JsonResponse({'msg': '0'})


@permission_required('myadmin.edit_goods', raise_exception=True)
def editgoods(request):
    gid = request.GET.get('id')

    if request.method == 'GET':
        types = cate_views.tab() #############################################3
        goods = models.Goods.objects.get(id=gid)
        return render(request, 'myadmin/goods/editgoods.html', {'types': types, 'goods': goods})
    elif request.method == 'POST':
        goods = models.Goods.objects.get(id=gid)

        g = request.POST.dict()
        g.pop('csrfmiddlewaretoken')

        goods.title = g['title']
        goods.price = g['price']
        goods.ordernum = g['ordernum']

        #################
        # cid = request.POST.get('cateid')
        # print('cid',cid)
        # cate = models.Cates.objects.get(id=cid)
        # print('cate', cate)
        # goods.cateid_id=cate

        file = request.FILES.get('g_url')
        # if not file:
        #     return HttpResponse('<script>alert("请选择图片");history.back(-1);</script>')
        # g_url = user_views.upload(file)
        # goods.g_url = g_url
        
        # if not file: # 若你没有修改, 直接点击, type=file 没图片
        #     return HttpResponse('<script>alert("请选择图片");history.back(-1);</script>')
        # elif file: # 若你修改了, 传有图
        #     # 右头像上传，要吧旧投头像删除
        #     # /dajngo07/py17/shop    ./static/pics/1547686265.6370358.png
        #     os.remove('.'+goods.g_url)
        #     g_url=user_views.upload(file)
        #     goods.g_url=g_url

        if file: # 若你修改了, 传有图
            # 右头像上传，要吧旧投头像删除
            # /dajngo07/py17/shop    ./static/pics/1547686265.6370358.png
            os.remove('.'+goods.g_url)
            g_url=user_views.upload(file)
            goods.g_url=g_url


        goods.ginfo = g['ginfo']
        goods.save()

        return HttpResponse('<script>location.href="' + reverse('myadmin_goodlist') + '";</script>')