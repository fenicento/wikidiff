from django.conf.urls import patterns, include, url
from wikitoc import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^lookup/(?P<voice>\w+).*$', views.lookup, name='lookup'),
)
