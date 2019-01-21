from django.db import models

# Create your models here.
# 用户模型
class Users(models.Model):
    # 用户名  密码  手机号  性别 年龄 状态 添加时间  头像
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    sex = models.CharField(max_length=1)
    age = models.CharField(max_length=3)
    head_url = models.CharField(max_length=100)
    # 为0:正常  1  2
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

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