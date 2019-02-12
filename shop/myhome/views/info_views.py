from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from myadmin import models
from django.core.urlresolvers import reverse
import os,time
from shop.settings import BASE_DIR


def myhome_info(request):
    # 接受商品的id 查询商品信息返回
    gid = request.GET.get('id')
    gobj = models.Goods.objects.get(id=gid)
    return render(request, 'myhome/goodsinfo.html', {'ginfo': gobj})

# 添加购物
def addcar(request):
    try:
        # 接受商品的id 和 数量 获取用的id
        info = request.GET.dict()
        # 获取商品的对象
        gobj = models.Goods.objects.get(id=info['gid'])
        # 获取用户对象
        uobj = models.Users.objects.get(id=request.session['userinfo']['uid'])
        
        # 判断 当前用户 有没有添加当前的这个商品  ###########################
        flag = models.Car.objects.filter(uid=uobj.id).filter(gid=gobj.id) 
        if flag.count():
            # 获取商品做更新
            for i in flag:
                i.num += int(info['num'])
                n = i.num
                i.save()
        else:
            # 入库
            car = models.Car()
            car.num=int(info['num'])
            car.gid = gobj
            car.uid = uobj
            n = car.num
            car.save()

        return JsonResponse({"msg": 1, "info": "添加成功", 'n': n})
    except:
        return JsonResponse({"msg": 0, "info": "添加失败"})


# 购物车页面
def carpage(request):
    # 查询当前用户的购物车
    uid = request.session.get('userinfo')
    if not uid:
        return HttpResponse('<script>alert("对不起,您没有登录!");location.href="' + reverse('myhome_login') + '";</script>')
    # 查询用户
    user = models.Users.objects.get(id=uid['uid'])
    # 根据外键查询用户购物车里有多少商品
    cgoods = user.car_set.all()
    print(cgoods) # <QuerySet [<Car: Car object>, <Car: Car object>]>
    return render(request, 'myhome/cart.html', {'cgoods': cgoods})

# 修改数量
def caredit(request):
    # 接受数量和cid
    cinfo = request.GET.dict()
    print(cinfo)
    # 根据 id 查询商品
    cobj = models.Car.objects.get(id=cinfo['cid'])
    # 修改数量
    cobj.num = int(cinfo['num'])
    cobj.save()

    return JsonResponse({'error': 1, 'msg': '修改成功'})

def cardel(request):
    cid = request.GET.get('cid')
    c = models.Car.objects.get(id=cid)
    c.delete()
    print(c.num, c.gid.price)
    return JsonResponse({'msg': '1', 'num': c.num, 'price': c.gid.price})

# 确认订单页
def confirm(request):
    # 接受购物车的id
    cart = request.GET.get('cid').split(',')
    cargoods = models.Car.objects.filter(id__in=cart)

    # 返回一级城市的数据
    citys = models.Citys.objects.filter(upid=0)

    # 当前用户的收货地址
    userobj = models.Users.objects.get(id=request.session['userinfo']['uid'])
    address = userobj.address_set.all()
    print(address.values())

    return render(request,'myhome/pay.html',{'cargoods':cargoods,'citys':citys,'address':address})

# 城际联动
def getcitys(request):
    # 接受upid
    upid = request.GET['upid']
    citys = models.Citys.objects.filter(upid=upid).values()
    return JsonResponse(list(citys),safe=False)

# 存地址
def saveaddress(request):
    

    # 接受
    addinfo = request.GET.dict()
    # 存数据
    address = models.Address()

    add = models.Address.objects.filter(uid=request.session['userinfo']['uid']).count()
    if add == 0:
        address.isselect = 1 ##########
    else:
        address.isselect = 0

    address.name=addinfo['name']
    address.phone=addinfo['phone']
    address.sheng=models.Citys.objects.get(id=addinfo['sheng']).name
    address.shi=models.Citys.objects.get(id=addinfo['shi']).name
    address.xian=models.Citys.objects.get(id=addinfo['xian']).name
    address.addinfo=addinfo['addinfo']




    address.uid = models.Users.objects.get(id=request.session['userinfo']['uid'])
    address.save()
    return JsonResponse({'error':0,'msg':'添加成功'})

# 生成订单 ###########################
def createorder(request):
    oinfo = request.POST.dict()
    print(oinfo)
    # 订单
    order = models.Order()
    order.uid = models.Users.objects.get(id = request.session['userinfo']['uid'])
    order.phone = models.Address.objects.get(id=oinfo['dizhi']).phone 
    order.name = models.Address.objects.get(id=oinfo['dizhi']).name
    # 地址
    sheng = models.Address.objects.get(id=oinfo['dizhi']).sheng
    shi = models.Address.objects.get(id=oinfo['dizhi']).shi
    xian = models.Address.objects.get(id=oinfo['dizhi']).xian
    addinfo = models.Address.objects.get(id=oinfo['dizhi']).addinfo
    print(addinfo)
    order.addinfo = sheng+shi+xian+addinfo

    order.wl = int(oinfo['wuliu'])
    order.pay = int(oinfo['zhifu'])

    order.total=0
    order.save()

    
    total=0
    carts = models.Car.objects.filter(id__in=oinfo['car'].split(','))
    for i in carts:
        # 订单详情
        orderinfo = models.Orderinfo()
        orderinfo.orderid = order
        orderinfo.num = i.num
        orderinfo.price = i.gid.price
        orderinfo.gid = i.gid
        orderinfo.save()
        total += i.num*i.gid.price
        i.delete()

    order.total = total
    order.save()


    # 跳转到支付
    return HttpResponse('<script>location.href="'+reverse('myhome_order_pay')+'?orderid='+str(order.id)+'"</script>')
    # return HttpResponse('ok')


# 订单支付
def myhome_order_pay(request):
    # 接收订单号
    orderid = request.GET.get('orderid')
    # 获取订单对象
    order = models.Order.objects.get(id=orderid)

    # 获取支付对象
    alipay = Get_AliPay_Object()

    # 生成支付的url
    query_params = alipay.direct_pay(
        subject="魅族旗舰官网",  # 商品简单描述
        out_trade_no = orderid,# 用户购买的商品订单号
        total_amount = order.total,  # 交易金额(单位: 元 保留俩位小数)
    )

    # 支付宝网关地址（沙箱应用）
    pay_url = settings.ALIPAY_URL+"?{0}".format(query_params)  
    # 页面重定向到支付页面
    return redirect(pay_url)



# 删除地址
def deladdress(request):
    aid = request.GET.get('aid')
    print(aid)
    address = models.Address.objects.get(id=aid)
    print(address)
    address.delete()

    return JsonResponse({'msg': '成功'})


# 订单
def order(request):
    order = models.Order.objects.filter(uid=request.session['userinfo']['uid'])

    lis = []
    for i in order:
        orderinfo = i.orderinfo_set.all()
        for j in orderinfo:
            lis.append(j)
    print(lis)

    data = {'order': order, 'lis': lis}

    return render(request, 'myhome/order.html', data)

# 删除订单
def delorder(request):
    oid = request.GET.get('oid')
    o = models.Order.objects.get(id=int(oid))
    oi = o.orderinfo_set.all()
    o.delete()
    oi.delete()
    return JsonResponse({'msg': '成功', 'error': 0})

# 订单详情
def orderinfo(request):
    uid = request.session['userinfo']['uid']
    oid = request.GET.get('oid') # 订单id
    user = models.Users.objects.get(id=uid) # 登录用户

    order = models.Order.objects.get(id=oid) # 订单

    orderinfo = order.orderinfo_set.all() # 订单详情

    address = user.address_set.get(isselect=1) # 地址

    return render(request, 'myhome/orderinfo1.html', {'address': address, 'order': order, 'orderinfo': orderinfo})

# 个人中心
def information(request):
    if request.method == 'GET':
        if not request.session.get('userinfo'):
            return HttpResponse('<script>alert("您没有登录,请登录");location.href="' + reverse('myhome_login') + '";</script>')
        else:
            user = models.Users.objects.get(id=request.session['userinfo']['uid'])
            address = user.address_set.all()
            return render(request, 'myhome/information.html', {'user': user, 'address': address})
    elif request.method == 'POST':
        user = request.POST.dict()
        user.pop('csrfmiddlewaretoken')
        uid = request.session['userinfo']['uid']
        request.session['userinfo']['vipuser'] = user['username']
        userinfo = models.Users.objects.get(id=uid)

        file = request.FILES.get('head_url')
        # print(file)
        # print(os.getcwd())
        if file: # 若你修改了, 传有图
            # print('file', file)
            # 右头像上传，要吧旧投头像删除
            # /dajngo07/py17/shop    ./static/pics/1547686265.6370358.png

            os.remove('.'+userinfo.head_url)  # /static/pics/1548487587.7164772.jpg
            head_url=upload(file)
            userinfo.head_url=head_url
  
        userinfo.username = user['username']
        userinfo.sex = user['sex']
        userinfo.age = user['age']
        userinfo.phone = user['phone']
        userinfo.save()

        return HttpResponse('<script>alert("修改成功");location.href="' + reverse('myhome_information') + '";</script>')

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





# 个人中心-地址管理
def address(request):

    user = models.Users.objects.get(id=request.session['userinfo']['uid'])
    address = user.address_set.all()

    citys = models.Citys.objects.filter(upid=0)

    if request.method == 'GET':
        return render(request, 'myhome/address.html', {'address': address, 'citys': citys})
    elif request.method == 'POST':
        
        return JsonResponse({'error':0,'msg':'添加成功'})

# pay.html 设为默认地址
def updateselect(request):
    
    aid = request.GET.get('aid')
    print(aid)

    uid = request.session['userinfo']['uid']
    user = models.Users.objects.get(id=uid)

    address0 = user.address_set.all().update(isselect=0)

    add = models.Address.objects.get(id=aid)
    add.isselect = 1
    add.save()

    return JsonResponse({'msg': 'success', 'aid': aid})     
    # return HttpResponse('ok')

# 订单详情-查看物流
def logistics(request):
    oid = request.GET.get('oid')
    print('===========',oid)
    order = models.Order.objects.get(id=int(oid))
    return render(request, 'myhome/logistics.html', {'order': order})



# 回调视图函数
# 支付宝回调地址
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def myhome_pay_result(request):
    # 获取对象
    alipay = Get_AliPay_Object()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        print('------------------开始------------------')
        print('POST验证', status)
        print(post_dict)
        out_trade_no = post_dict['out_trade_no']

        # 修改订单状态
        models.Order.objects.filter(id=out_trade_no).update(status=1)
        print('------------------结束------------------')
        # 修改订单状态：获取订单号
        return HttpResponse('POST返回')
    else:
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('==================开始==================')
        print('GET验证', status)
        print('==================结束==================')
        # 支付成功后可以跳转到 个人中心的订单页面
        # return HttpResponse('<script>alert("支付成功");支付完成</script>')
        return HttpResponse('<script>alert("支付成功");location.href="' + reverser('myhome_order') + '";</script>')


from shop import settings
from utils.pay import AliPay

# AliPay 对象实例化
def Get_AliPay_Object():
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,# APPID （沙箱应用）
        app_notify_url=settings.ALIPAY_NOTIFY_URL, # 回调通知地址
        return_url=settings.ALIPAY_NOTIFY_URL,# 支付完成后的跳转地址
        app_private_key_path=settings.APP_PRIVATE_KEY_PATH, # 应用私钥
        alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,  # 支付宝公钥
        debug=True,  # 默认False,
    )
    return alipay    