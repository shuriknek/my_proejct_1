
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
    url(r'^cookie_detect_view', views.cookie_detect_view, name='cookie_detect_view'),
    url(r'^cookie_set_view', views.cookie_set_view, name='cookie_set_view'),
]
