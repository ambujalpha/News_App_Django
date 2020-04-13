from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^comment/add/news/(?P<pk>\d+)/$', views.news_cm_add, name='news_cm_add'),
    url(r'^comments/list/$', views.comments_list, name='comments_list'),
    url(r'^comments/del/(?P<pk>\d+)/$', views.comments_del, name='comments_del'),
    url(r'^comments/confirme/(?P<pk>\d+)/$', views.comments_confirme, name='comments_confirme'),
]
