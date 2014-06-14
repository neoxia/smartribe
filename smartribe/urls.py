from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf.urls.static import static
from smartribe import settings

urlpatterns = patterns('',
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'', 'serve', {'path': 'angular/smartribe/app/index.html'}),
    )
