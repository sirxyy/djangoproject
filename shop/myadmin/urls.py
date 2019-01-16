from django.conf.urls import url
from . import views

# https://github.com/sirxyy/djangoproject

urlpatterns = [
    url(r'^$', views.index, name="myadmin_index"),
    url(r'^vipuser/$', views.vipuser, name="myadmin_vipuser"),
    url(r'^adduser/$', views.adduser, name="myadmin_adduser"),

]