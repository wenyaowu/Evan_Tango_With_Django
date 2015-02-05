__author__ = 'evanwu'
from django.conf.urls import patterns, url
from rango import views

# What does url.py do?
# When one send a request to our server,
# Django will come to url.py to find the corresponding match
# of the url and use url() to make a call/request to match view in view.py

# Django loads that Python module and looks for the variable urlpatterns.
# This should be a Python list, in the format
# returned by the function django.conf.urls.patterns().
urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),  # url(mapping address, view, name of view)
                       url(r'^about/$', views.about, name='about'), # This line will just call the view.about(request)
                       url(r'^add_category/$', views.add_category, name='add_category'),
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
                       url(r'^goto/$', views.track_url, name='goto'),
                       # (?P<name>pattern)
                       # This line will call the function views.category(request, 'category_name_slug'=....)
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
                       url(r'^restricted/$', views.restricted, name='restricted'),
                       url(r'^search/$', views.search, name='search'),
)