from django.conf.urls import patterns, url, include
from django.contrib import admin
from smartribe import settings

urlpatterns = patterns('',
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': ''}))

#if settings.DEBUG:
    #urlpatterns += url(r'(?P<path>.*)$', 'django.views.static.serve',
             #{'document_root': './angular/smartribe/app/'}),
