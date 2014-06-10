from django.conf.urls import patterns, url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'permissions', views.PermissionViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'communities', views.CommunityViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
                       url(r'^v1/', include(router.urls)),
                       url(r'^v1/auth/', include('rest_framework.urls',
                                                 namespace='rest_framework')
                           ),
                       url(r'^v1/auth/createuser', 'api.views.Create_User')
                       )
urlpatterns += patterns('',
    url(r'^v1/api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token')
)
