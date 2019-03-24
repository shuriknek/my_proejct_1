
#-*-coding:utf-8;-*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reg_view$', views.reg_view, name='reg_view'),
    url(r'^login_view$', views.login_view,  name='login_view'),
    url(r'^contact_view$', views.contact_view, name='contact_view'),
    url(r'^regulat_view$', views.regulat_view, name='regulat_view'),
    url(r'^set_cookie$', views.set_cookie, name='set_cookie'),
    url(r'^verify_login', views.verify_login, name='verify_login'),
]
