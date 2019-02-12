from django.db import models

# Create your models here.
# 用户模型
class Users(models.Model):
    # 用户名  密码  手机号  性别 年龄 状态 添加时间  头像
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    sex = models.CharField(max_length=1, null=True)
    age = models.CharField(max_length=3, null=True)
    head_url = models.CharField(max_length=100, null=True)
    # 为0:正常  1  2
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("show_users", "查看会员管理"),
            ("insert_users", "添加会员"),
            ("edit_users", "修改会员"),
            ("del_users", "删除会员"),
        )

# 商品的分类
class Cates(models.Model):
    # id  name        upid      paths
    #  1  手机          0         0，
    #  2  家电          0         0，
    #  3  小米手机       1         0,1,
    #  4  小电视         2        2
    #  5  米8           3         0,1,3,
    #  6  米8m          5         0,1,3,5
    name = models.CharField(max_length=50)
    upid = models.IntegerField()
    paths = models.CharField(max_length=50)

    class Meta:
        permissions = (
            ("show_cates", "查看商品分类管理"),
            ("insert_cates", "添加商品分类"),
            ("edit_cates", "修改商品分类"),
            ("del_cates", "删除商品分类"),
        )

# 商品的管理
class Goods(models.Model):
    # id titlt order_num status price img clicknum addtime 
    title = models.CharField(max_length=100)
    g_url = models.CharField(max_length=200)
    price = models.IntegerField()
    ordernum = models.IntegerField()
    ginfo = models.TextField()
    
    status = models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    cateid = models.ForeignKey(to="Cates", to_field="id")

    class Meta:
        permissions = (
            ("show_goods", "查看商品管理"),
            ("insert_goods", "添加商品"),
            ("edit_goods", "修改商品"),
            ("del_goods", "删除商品"),
        )

# 购物车
class Car(models.Model):
    gid = models.ForeignKey(to="Goods", to_field="id")
    num = models.IntegerField()
    uid = models.ForeignKey(to="Users", to_field="id")

# 用户的收货人地址
class Address(models.Model):
    # id name phone sheng shi xian addinfo uid
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    sheng = models.CharField(max_length=100)
    shi = models.CharField(max_length=100)
    xian = models.CharField(max_length=100)
    addinfo = models.CharField(max_length=255)

    uid = models.ForeignKey(to="Users", to_field="id")

    isselect = models.IntegerField(default=0)

    class Meta:
        permissions = (
            ("show_address", "查看地址管理"),
            ("insert_address", "添加地址"),
            ("edit_address", "修改地址"),
            ("del_address", "删除地址"),
        )

class Citys(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    upid = models.IntegerField()

    class Meta():
        db_table = 'citys'

# 订单 
class Order(models.Model):
    # uid phone address total wl pay uid status
    uid = models.ForeignKey(to="Users", to_field="id")
    phone = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    addinfo = models.CharField(max_length=255)
    total = models.IntegerField()
    # 0 顺丰 1 申通 2圆通
    wl = models.IntegerField()

    pay = models.IntegerField()

    status = models.IntegerField(default=0)

    createtime = models.DateTimeField(auto_now_add=True)

    paytime = models.DateTimeField(null=True)

    class Meta:
        permissions = (
            ("show_order", "查看订单管理"),
            ("insert_order", "添加订单"),
            ("edit_order", "修改订单"),
            ("del_order", "删除订单"),
        )

class Orderinfo(models.Model):
    # gid  orderid num price
    orderid =  models.ForeignKey(to="Order",to_field="id")
    gid = models.ForeignKey(to="Goods",to_field="id")
    num = models.IntegerField()
    price = models.IntegerField()