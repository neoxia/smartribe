from django.conf.urls import patterns, url, include
from rest_framework import routers
from api.views import viewsOLD
from api.views import user_view
from api.views import profile_view
from api.views import community_view
from api.views import member_view


router = routers.DefaultRouter()
router.register(r'users', user_view.UserViewSet)
router.register(r'groups', viewsOLD.GroupViewSet)
router.register(r'permissions', viewsOLD.PermissionViewSet)
router.register(r'profiles', profile_view.ProfileViewSet)
router.register(r'communities', community_view.CommunityViewSet)
router.register(r'members', member_view.MemberViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
                       url(r'^v1/', include(router.urls)),
                       url(r'^v1/auth/', include('rest_framework.urls',
                                                 namespace='rest_framework')
                           )
                       )
urlpatterns += patterns('',
    url(r'^v1/api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token')
)
