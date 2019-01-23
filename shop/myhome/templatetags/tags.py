from django import template
from myadmin import models
register = template.Library()



# 自定义标签
from django.utils.html import format_html
@register.simple_tag
def nav():
    # 查询所有的一级分类
    cates1 = models.Cates.objects.filter(upid=0)
    str1 = ''
    for i in cates1:
        str1 += '''
            <li class="layout-header-nav-item"><a href="/static/myhome/list.html" class="layout-header-nav-link">{name}</a></li>
        '''.format(name=i.name)
    print(str1)
    return format_html(str1)