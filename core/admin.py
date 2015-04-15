from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from core.admins.community import CommunityAdmin, LocalCommunityAdmin, TransportCommunityAdmin
from core.admins.location import LocationAdmin
from core.admins.meeting_point import MeetingPointAdmin
from core.admins.member import MemberAdmin
from core.admins.message import MessageAdmin
from core.admins.offer import OfferAdmin
from core.admins.request import RequestAdmin
from core.models import Member, Location, MeetingPoint, Meeting
from core.models.donation import Donation
from core.models.skill import SkillCategory
from .models import Profile, Evaluation, Message, Notification
from .models import Community
from .models import TransportCommunity
from .models import LocalCommunity
from .models import Skill
from .models import Request
from .models import Offer


admin.autodiscover()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'get_profile_completion', 'get_user_level', 'get_title',
                    'mail_notification', 'early_adopter', 'donor')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(SkillCategory)
admin.site.register(Skill)

admin.site.register(Community, CommunityAdmin, )
admin.site.register(LocalCommunity, LocalCommunityAdmin)
admin.site.register(TransportCommunity, TransportCommunityAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(MeetingPoint, MeetingPointAdmin)
admin.site.register(Member, MemberAdmin)

admin.site.register(Request, RequestAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Evaluation)
admin.site.register(Meeting)



admin.site.register(Notification)
admin.site.register(Donation)
