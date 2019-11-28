from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^index/$',index),#登录

    url(r'^fankuiye/$',fankuiye), #反馈页接口
    url(r"^quanxian/$",quanxian),
    url(r"^pingtaishuju/$",pingtaishuju),#通过用户权限获取赛事数据
    url(r'^tijiaofankui/$',tijiaofankui), #提交反馈并发送邮件

    url(r'^fankuijieguo/$',fankuijieguo),#反馈结果页
    url(r'^fjieguo/$', fjieguo),  # 反馈结果数据接口
    url(r'^sousuo/$',sousuo), # 搜索接口
    url(r'^tijiaoinfo/$',tijiaoinfo)#运营接收反馈
]

#备用接口
urlpatterns += [
    url(r'^Ashuju/$', Ashuju),  # A平台数据
    url(r'^Bshuju/$', Bshuju),  # B平台数据
    url(r"^Cshuju/$", Cshuju),  # C平台数据
]



urlpatterns += [
    url(r'^duo/$', duo), #测试多条件查询
    url(r'^testajax/$',testajax),#测试ajax接收值
    url(r'^sessioninfo/$', sessioninfo),  # 测试当前登录用户显示接口

    url(r'^dd/$', dd),#测试数据格式处理
    url(r'^addyunyingdata/$',addyunyingdata),#运营数据存入数据库

    url(r'^getoIndex/', getoIndex),  # wsx协议
    url(r'^echo$', echo),
]












