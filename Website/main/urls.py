from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^login/$', views.mylogin, name='mylogin'),
    url(r'^logout/$', views.mylogout, name='mylogout'),
    url(r'^panel/setting/$', views.site_setting, name='site_setting'),
    url(r'^panel/about/setting/$', views.about_setting, name='about_setting'),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
