from django.shortcuts import render
from django.http import HttpResponse
from myadmin import models


def myhome_list(request, cid, bid):
    # 根据参数查询当前选择的是哪一个一级分类
    ob1 = models.Cates.objects.get(id=cid)
    # 当前一级分类下的二级分类
    ob2 = models.Cates.objects.filter(upid=cid)
    # 遍历当前一级分类下的所有二级分类
    goods = []
    bid = int(bid)
    for cate2 in ob2:
        # 判断 r如果点的事一级分类 cid=1 bid=0
        # cid = 1 bid = 11
        # if cate2.id != bid and bid != 0:
        #     continue
        # # 根据二级分类对象查询 当前一级分类下二级分类的所有商品
        # goods.append(cate2.goods_set.all())

        # 判断是否是一级分类
        if bid == 0:
            # 一级分类
            goods.append(cate2.goods_set.all())
        else:
            # 二级分类,判断获取哪个二级分类,然后将二级分类的数据写入到列表
            if cate2.id == bid:
                goods.append(cate2.goods_set.all())
        print(goods)
    content = {'cate1': ob1, 'cate2': ob2, 'goods': goods, 'color': bid}
    return render(request, 'myhome/list.html', content)