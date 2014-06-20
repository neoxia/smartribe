from django.conf.urls import patterns, url, include
from rest_framework import routers
from api.views import user
from api.views import profile
from api.views import community
from api.views import member


router = routers.DefaultRouter()
router.register(r'users', user.UserViewSet)

router.register(r'profiles', profile.ProfileViewSet)
router.register(r'communities', community.CommunityViewSet)
router.register(r'members', member.MemberViewSet)

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
