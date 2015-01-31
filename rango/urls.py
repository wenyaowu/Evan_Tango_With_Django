__author__ = 'evanwu'
from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),  # url(mapping address, view, name of view)
                       url(r'^about/', views.about, name='about'),
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'))