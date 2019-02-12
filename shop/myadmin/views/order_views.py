from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from .. import models
from django.contrib.auth.decorators import permission_required

# @permission_required('myadmin.show_order', raise_exception=True)
def orderlist(request):
    orders = models.Order.objects.all()

    types = request.GET.get('type') # name: 
    print('=====',types)
    search = request.GET.get('search')
    if types:
        if types == 'all':
            from django.db.models import Q
            orders = models.Order.objects.filter(Q(id__contains=search)|Q(name__contains=search)|Q(phone__contains=search)|Q(addinfo__contains=search))
        elif types == 'uid':
            orders = models.Order.objects.filter(id__contains=search)
        elif types == 'uname':
            orders = models.Order.objects.filter(name__contains=search)
        elif types == 'uphone':
            orders = models.Order.objects.filter(phone__contains=search)
        elif types == 'uaddress':
            orders = models.Order.objects.filter(addinfo__contains=search)

    # 实例化分页对象
    p = Paginator(orders, 5)

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

    return render(request, 'myadmin/orders/orderlist.html', {'orders': page1, 'prange': prange, 'page': page, 'sumpage': sumpage})



def orderinfo(request):
    oid = request.GET.get('oid')
    # print('oid', oid)
    order = models.Order.objects.get(id=oid)
    # print('order', order)
    orderinfos = order.orderinfo_set.all()
    # print('orderinfos', orderinfos)
    # return render(request, 'myadmin/orders/orderinfo.html', {'order': order, 'orderinfos': orderinfos})


    types = request.GET.get('type') # name: 
    print('=====',types)
    search = request.GET.get('search')
    if types:
        if types == 'all':
            from django.db.models import Q
            order = models.Order.objects.filter(Q(name__contains=search)|Q(addinfo__contains=search))
        elif types == 'uname':
            order = models.Order.objects.filter(name__contains=search)
        elif types == 'uaddress':
            order = models.Order.objects.filter(addinfo__contains=search)

    # orderinfos = order.orderinfo_set.all()

    # 实例化分页对象
    p = Paginator(orderinfos, 1) # 一页2条
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
    return render(request, 'myadmin/orders/orderinfo.html', {'order': order, 'orderinfos': page1, 'prange': prange, 'page': page, 'sumpage': sumpage})
