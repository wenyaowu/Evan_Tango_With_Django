from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings # Allow urls.py access setting.py

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Evan_Tango_With_Django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')), # Tell the project to get url from rango.urls if encounter /rango/ in URL
    (r'^accounts/', include('registration.backends.simple.urls')),
    (r'^password/', include('registration.backends.simple.urls')),
)

if settings.DEBUG: # If the DEBUG mode is true (See setting.py), then do this
    urlpatterns += patterns(
        'django.views.static', # This handle the dispatching of uploaded media files
        (r'^media/(?P<path>.*)', # When any files requested with URL starting with media/
        'serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
