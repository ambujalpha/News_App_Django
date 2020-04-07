from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^panel/manager/list/$', views.manager_list, name='manager_list'),
    url(r'^panel/manager/del/(?P<pk>/d+)$', views.manager_del, name='manager_del'),
]