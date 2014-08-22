from django.conf.urls import patterns, url, include
from rest_framework import routers

from api.views import user
from api.views import profile
from api.views import community
from api.views import local_community
from api.views import transport_community
from api.views import media
from api.views import skill
from api.views import faq
from api.views import suggestion
from api.views import inappropriate
from api.views import request
from api.views import offer
from smartribe.settings import MEDIA_ROOT


router = routers.DefaultRouter()
router.register(r'users', user.UserViewSet)
router.register(r'profiles', profile.ProfileViewSet)
router.register(r'communities', community.CommunityViewSet)
router.register(r'local_communities', local_community.LocalCommunityViewSet)
router.register(r'transport_communities', transport_community.TransportCommunityViewSet)
router.register(r'skill_categories', skill.SkillCategoryViewSet)
router.register(r'skills', skill.SkillViewSet)
router.register(r'faq', faq.FaqViewSet)
router.register(r'suggestions', suggestion.SuggestionViewSet)
router.register(r'inappropriates', inappropriate.InappropriateViewSet)

router.register(r'requests', request.RequestViewSet)
router.register(r'offers', offer.OfferViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
                       url(r'^v1/', include(router.urls)),
                       url(r'^v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
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
