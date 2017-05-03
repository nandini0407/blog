from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<p_id>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^new/$', views.post_new, name='post_new'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<p_id>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^(?P<p_id>[0-9]+)/update$', views.post_update, name='post_update'),
    # url(r'^(?P<p_id>[0-9]+)/destroy$', views.post_destroy, name='post_destroy')
]
