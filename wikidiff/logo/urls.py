from django.conf.urls import patterns, include, url
from wikitoc import views
from logo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^find$', views.find),
    
)
