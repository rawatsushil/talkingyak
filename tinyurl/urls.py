from django.conf.urls import url

from . import views

urlpatterns = [
    url('short-url', views.CreateTinyUrlView.as_view(), name='tinyUrl'),
    url('meta-info/(?P<short_id>[\w\-]+)/$', views.ShortUrlMetaInfo.as_view(), name='tinyUrlMeta')
]