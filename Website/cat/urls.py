from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^panel/category/list/$', views.cat_list, name='cat_list'),

]