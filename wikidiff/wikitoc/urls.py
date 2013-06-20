from django.conf.urls import patterns, include, url
from wikitoc import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^lookup/(?P<voice>\w+).*$', views.init_work),
    url(r'^poll_state$', views.poll_state,name='poll_state'),
    url(r'^progress$', views.poll_state),
    url(r'^example$', views.example),
)
