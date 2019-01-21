from django.conf.urls import url
from .views import user_views, index_views, cate_views, goods_views

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

    
]