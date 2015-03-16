from django.contrib import admin

from core.admins.community import CommunityAdmin, LocalCommunityAdmin, TransportCommunityAdmin
from core.admins.location import LocationAdmin
from core.admins.meeting_point import MeetingPointAdmin
from core.admins.member import MemberAdmin
from core.admins.message import MessageAdmin
from core.admins.offer import OfferAdmin
from core.admins.request import RequestAdmin
from core.models import Member, Location, MeetingPoint, Meeting
from core.models.skill import SkillCategory
from .models import Profile, Evaluation, Message, Notification
from .models import Community
from .models import TransportCommunity
from .models import LocalCommunity
from .models import Skill
from .models import Request
from .models import Offer


admin.autodiscover()

admin.site.register(Profile)
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
