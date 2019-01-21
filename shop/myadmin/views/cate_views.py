from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import time, os
from django.core.urlresolvers import reverse
from .. import models
from shop.settings import BASE_DIR
from django.core.paginator import Paginator


def tab():
    cates = models.Cates.objects.extra(select = {'newpath': 'concat(paths, id)'}).order_by('newpath')
    for i in cates:
        num = i.paths.count(',') - 1
        i.newname = num * '|____'
    return cates


# Create your views here.
def addcate(request):
    if request.method == 'GET':
        # 将所有的类型返回
        # cates = models.Cates.objects.all()
        cates = tab()
        return render(request, 'myadmin/cate/addcate.html', {'cates': cates})
    elif request.method == 'POST':
        # 接受upid 通过upid来判断是不是顶级分类
        upid = request.POST.get('upid')
        name = request.POST.get('name')
        # print(pid)
        # print(name)

        if upid == '0':
            cate = models.Cates()
            cate.name = name
            cate.upid = int(upid)
            cate.paths = '0,'
            cate.save()
        else:
            # 根据upid找父级 paths
            pobj = models.Cates.objects.get(id=upid)
            c = models.Cates()
            c.name = name
            c.upid = pobj.id
            c.paths = pobj.paths + upid + ','
            c.save()

        # 接受数据添加数据
        return redirect(reverse('myadmin_addcate'))

def catelist(request):
    # 查询所有的分类
    cates = models.Cates.objects.all()
    # select *,concat(paths,id) as newpath from myadmin_cates order by newpath;
    cates = models.Cates.objects.extra(select = {'newpath': 'concat(paths, id)'}).order_by('newpath')
    # for i in cates:
    #     num = i.paths.count(',') - 1
    #     i.newname = num * '|____'

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
            cates = cates.filter(Q(id__contains=search)|Q(name__contains=search)|Q(upid__contains=search))
        elif types=='name':
            cates = cates.filter(name__contains=search)
        elif types=='upid':
            cates = cates.filter(upid__contains=search)
        elif types == 'id':
            cates = cates.filter(id__contains=search)
    for i in cates:
        num = i.paths.count(',') - 1
        i.newname = num * '|____'

    # cates = tab()
    # 实例化分页对象
    p = Paginator(cates, 10)
    #一共可以分多少页
    sumpage=p.num_pages
    # 取第几页的数据
     # 接受用户的页码
    page = int(request.GET.get('p',1))
    # 第几页的数据
    page1 = p.page(page)
    # 判断 如果用输入的页码<=3 显示前五个页码
    if page<=3:
        # 页码的迭代序列  [1,2,3,4,5,6,7]
        prange = p.page_range[:5]
    elif page+2>=sumpage:
        prange = p.page_range[-5:]
    else:
        prange = p.page_range[page-3:page+2]
    
    return render(request, 'myadmin/cate/catelist.html', {'cates':page1,'prange':prange,'page':page,'sumpage':sumpage})

    # cates = tab()
    # return render(request, 'myadmin/cate/catelist.html', {'cates': cates})

def delcate(request):
    # 接受id
    pid = int(request.GET.get('pid')) # 就是id
    cnum = models.Cates.objects.filter(upid=pid).count() # 找子类
    # 判断有没有子分类
    if cnum:
        # 有子类,不能删除
        return JsonResponse({'msg': 0})
    else:
        c = models.Cates.objects.get(id=pid)
        c.delete()
        return JsonResponse({ 'msg': 1 })

# 修改
def editcate(request):
    cid = int(request.GET.get('id'))
    cname = request.GET.get('name')
    try:
        cate = models.Cates.objects.get(id=cid)
        cate.name = cname
        cate.save()
        return JsonResponse({'msg': 1})

    except:
        return JsonResponse({'msg': 0})

