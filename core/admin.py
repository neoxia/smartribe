from django.contrib import admin
from core.models import Member, Location, MeetingPoint, Meeting, FaqSection, Faq, Inappropriate, Suggestion
from core.models.activation_token import ActivationToken
from core.models.skill import SkillCategory
from .models import Profile, Evaluation, Message
from .models import Community
from .models import TransportCommunity
from .models import LocalCommunity
from .models import Tos
from .models import Skill
from .models import Request
from .models import Offer
from .models import PasswordRecovery

admin.autodiscover()


class CommunityAdmin(admin.ModelAdmin):
    model = Community
    list_display = ['name']
    search_fields = ('name', 'description')


admin.site.register(Tos)
admin.site.register(ActivationToken)
admin.site.register(PasswordRecovery)
admin.site.register(Profile)
admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(Community, CommunityAdmin)
admin.site.register(LocalCommunity, CommunityAdmin)
admin.site.register(TransportCommunity, CommunityAdmin)
admin.site.register(Location)
admin.site.register(MeetingPoint)
admin.site.register(Member)
admin.site.register(Request)
admin.site.register(Offer)
admin.site.register(Evaluation)
admin.site.register(Message)
admin.site.register(Meeting)
admin.site.register(FaqSection)
admin.site.register(Faq)
admin.site.register(Inappropriate)
admin.site.register(Suggestion)


