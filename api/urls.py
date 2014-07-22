from django.conf.urls import patterns, url, include
from rest_framework import routers
from rest_framework.routers import Route
from api.views import user
from api.views import user_bis
from api.views import profile
from api.views import community
from api.views import member
from api.views import media
from api.views import skill
from api.views.user_bis import UserListView
from smartribe.settings import MEDIA_ROOT


class MyRouter(routers.DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated routes.
        # Generated using @action or @link decorators on methods of the viewset.
        Route(
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
            mapping={
                '{httpmethod}': '{methodname}',
            },
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/toto/test(?P<username>.*){trailing_slash}$',
            mapping={
                'get': 'list'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
  ]




router = routers.DefaultRouter()
#router = MyRouter()
router.register(r'users', user_bis.UserBisViewSet)
router.register(r'profiles', profile.ProfileViewSet)
router.register(r'communities', community.CommunityViewSet)
router.register(r'members', member.MemberViewSet)
router.register(r'skill_categories', skill.SkillCategoryViewSet)
router.register(r'skills', skill.SkillViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
                       url(r'^v1/', include(router.urls)),
                       url(r'^v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^v1/login/$', user_bis.LoginViewSet),
                       url(r'^v1/search(.*)$', UserListView.search),
                       #url(r'^v1/test/(?P<username>.+)/$', user_bis.UserBisViewSet),
)

urlpatterns += patterns('',
                        url(r'^v1/api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'))
#urlpatterns += patterns('',
                        #url(r'^v1/(?P<path>.*)$', 'django.views.static.serve',
                            #{'document_root': ''}))

urlpatterns += patterns('',
                        url(r'^v1/media/(?P<path>.*)$', media.MediaViewSet.get_media, {'document_root': MEDIA_ROOT}))

#urlpatterns += patterns('',
#                        url(r'^v1/recovery/recover_password', user.UserViewSet.recover_password),
#                        url(r'^v1/recovery/set_new_password', user.UserViewSet.set_new_password)
#)
