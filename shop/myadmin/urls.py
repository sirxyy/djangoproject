from django.conf.urls import url
from .views import user_views, index_views, cate_views, goods_views, order_views, authviews

# https://github.com/sirxyy/djangoproject

urlpatterns = [
    # 首页
    url(r'^$', index_views.index, name="myadmin_index"),



    # 用户管理
    url(r'^vipuser/$', user_views.vipuser, name="myadmin_vipuser"),
    url(r'^adduser/$', user_views.adduser, name="myadmin_adduser"),
    url(r'^deluser/$', user_views.deluser, name="myadmin_deluser"),
    url(r'^edituser/$', user_views.edituser, name="myadmin_edituser"),
    # 修改状态
    url(r'^changes/$', user_views.changes, name="myadmin_changes"),
    # 重置密码
    url(r'^respwd/$', user_views.respwd, name="myadmin_respwd"),



    # 商品的分类
    url(r'^addcate/$', cate_views.addcate, name="myadmin_addcate"),
    url(r'^listcate/$', cate_views.catelist, name="myadmin_catelist"),    
    url(r'^delcate/$', cate_views.delcate, name="myadmin_delcate"),
    url(r'^editcate/$', cate_views.editcate, name="myadmin_editcate"),



    # 商品管理
    url(r'^addgoods/$', goods_views.addgoods, name="myadmin_addgoods"),
    url(r'^goodsinsert/$', goods_views.goodsinsert, name="myadmin_goodsinsert"),
    url(r'^goodslist/$', goods_views.goodslist, name="myadmin_goodlist"),
    url(r'^delgoods/$', goods_views.delgoods, name="myadmin_delgoods"),
    url(r'^editgoods/$', goods_views.editgoods, name="myadmin_editgoods"),

    
    # 登录
    url(r'^login/$', authviews.myadminLogin, name="myadmin_login"),
    # yzm
    url(r'^verifycode/$', index_views.verifycode, name="myadmin_yzm"),
    # 退出登录
    url(r'^outlogin/$', authviews.myadminLogout, name="myadmin_out"),



    # 订单列表
    url(r'^orderlist/$', order_views.orderlist, name="myadmin_orderlist"),
    # 订单详情
    url(r'^orderinfo/$', order_views.orderinfo, name="myadmin_orderinfo"),
    # 删除订单
    url(r'^delorder/$', order_views.delorder, name="myadmin_delorder"),
    # 修改订单总价格
    url(r'^editprice/$', order_views.editprice, name="myadmin_editprice"),



    # 后台权限管理

    # 后台用户添加
    url(r'^auth/user/add/$', authviews.useradd, name="auth_user_add"),
    # 后台用户列表
    url(r'^auth/user/list/$', authviews.userlist, name="auth_user_list"),
    url(r'^auth/user/del/(?P<uid>[0-9]+)/$', authviews.userdel, name="auth_user_del"),


    # 后台组添加
    url(r'^auth/group/add/$', authviews.groupadd, name="auth_group_add"),
    # 后台组列表
    url(r'^auth/group/list/$', authviews.grouplist, name="auth_group_list"),
    url(r'^auth/group/edit/(?P<gid>[0-9]+)/$', authviews.groupedit, name="auth_group_edit"),


]