from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^api/', include('api.urls')),
)
