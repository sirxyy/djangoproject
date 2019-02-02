from django.conf.urls import url
from . views import index_views, list_views, info_views, safe_views

urlpatterns = [
    # 首页, 列表页, 详情页 
    url(r'^$', index_views.index, name="myhome_index"),
    url(r'^list/(?P<cid>[0-9]+)/(?P<bid>[0-9]+)/$', list_views.myhome_list, name="myhome_list"),
    url(r'^info/$', info_views.myhome_info, name="myhome_info"),

    # 登录, 注册, 验证码, 退出登录
    url(r'^login/$', index_views.myhome_login, name="myhome_login"),
    url(r'^register/$', index_views.myhome_register,name='myhome_register'),
    url(r'^sendmsg/$', index_views.sendmsg,name='myhome_sendmsg'),
    url(r'^out/$', index_views.myhome_outlogin, name="myhome_out"),
    url(r'^cardel/$', info_views.cardel, name="myhome_cardel"),

    # 购物车
    url(r'^addcar/$', info_views.addcar, name="myhome_car"),
    url(r'^carpage/$', info_views.carpage, name="myhome_carpage"),
    url(r'^caredit/$', info_views.caredit, name="myhome_caredit"),

    # 订单
    url(r'^confirm/$', info_views.confirm,name='myhome_confirm'),
    # 获取城市地址
    url(r'^getcitys/$', info_views.getcitys,name='myhome_getcitys'),
    # 存地址
    url(r'^saveaddress/$', info_views.saveaddress,name='myhome_saveaddress'),
    # 生成订单
    url(r'^createorder/$', info_views.createorder,name='myhome_createorder'),


    # 删除地址
    url(r'^deladdress/$', info_views.deladdress, name="myhome_deladdress"),
    # 个人中心-查看订单
    url(r'^order/$', info_views.order, name="myhome_order"),
    # 删除订单
    url(r'^delorder/$', info_views.delorder, name="myhome_delorder"),
    # 个人中心-订单的详情
    url(r'^orderinfo/$', info_views.orderinfo, name="myhome_orderinfo"),
    # 个人中心
    url(r'^information/$', info_views.information, name="myhome_information"),
    # 个人中心-地址管理
    url(r'^address/$', info_views.address, name="myhome_address"),
    # 个人中心-安全设置
    url(r'^safety/$', safe_views.safety, name="myhome_safety"),
    # 修改密碼
    url(r'^resetpwd/$', safe_views.resetpwd, name="myhome_resetpwd"),
    url(r'^verifyold/$', safe_views.verifyold, name="myhome_verifyold"),
    # 换绑手机
    url(r'^bindphone/$', safe_views.bindphone, name="myhome_bindphone"),


    # 设为默认地址 isselect
    url(r'^updateselect/$', info_views.updateselect, name="myhome_updateselect"),
    # 物流
    url(r'^logistics/$', info_views.logistics, name="myhome_logistics"),












    # 支付
    url(r'^myhome_order_pay/$', info_views.myhome_order_pay, name="myhome_order_pay"),
    # 支付宝回调
    url(r'^order/pay_result/$', info_views.myhome_pay_result, name="myhome_pay_result"),





   
    

]